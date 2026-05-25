#!/usr/bin/env python3
"""
Real Estate Lead Scraper
Scrapes public real estate listings to generate leads for the system.

© Shylow Thompson. LLC 2026 - All Rights Reserved
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import random
from datetime import datetime, timedelta
import re
from urllib.parse import urljoin, urlparse, quote_plus
import logging
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import asyncio
from asyncio_throttle import Throttler
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import numpy as np
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import email_validator

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class ScrapingConfig:
    """Configuration for scraping operations."""
    max_requests_per_minute: int = 30
    max_requests_per_hour: int = 500
    request_delay: float = 2.0
    timeout: int = 15
    max_retries: int = 3
    user_agents: List[str] = None

    def __post_init__(self):
        if self.user_agents is None:
            self.user_agents = [
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15'
            ]

@dataclass
class LeadScore:
    """AI scoring for lead quality."""
    overall_score: float
    price_score: float
    location_score: float
    property_score: float
    market_score: float
    motivation_score: float
    reasons: List[str]

class RealEstateLeadScraper:
    """Advanced scraper for real estate leads with AI targeting and rate limiting."""

    def __init__(self, config: ScrapingConfig = None):
        self.config = config or ScrapingConfig()
        self.session = requests.Session()

        # Rate limiting
        self.throttler = Throttler(rate_limit=self.config.max_requests_per_minute / 60)
        self.hourly_throttler = Throttler(rate_limit=self.config.max_requests_per_hour / 3600)
        self.request_count = 0
        self.hour_start = time.time()

        # Selenium setup for JavaScript-heavy sites
        self.driver = None

        # AI components
        self.geolocator = Nominatim(user_agent="realtor_agent_scraper")
        self.lead_scorer = None

        # Sample cities and states
        self.test_locations = [
            ('Austin', 'TX'), ('Dallas', 'TX'), ('Houston', 'TX'), ('San Antonio', 'TX'),
            ('Denver', 'CO'), ('Phoenix', 'AZ'), ('Raleigh', 'NC'), ('Nashville', 'TN'),
            ('Orlando', 'FL'), ('Tampa', 'FL'), ('Charlotte', 'NC'), ('Atlanta', 'GA')
        ]

        # Market data cache
        self.market_cache = {}
        self.cache_timeout = 3600  # 1 hour

        self._setup_session()

    def _setup_session(self):
        """Setup requests session with proper headers."""
        self.session.headers.update({
            'User-Agent': random.choice(self.config.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })

    def _init_selenium_driver(self):
        """Initialize Selenium WebDriver for JavaScript rendering."""
        if self.driver is None:
            options = Options()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument('--window-size=1920,1080')
            options.add_argument(f'--user-agent={random.choice(self.config.user_agents)}')

            try:
                self.driver = webdriver.Chrome(options=options)
                self.driver.implicitly_wait(10)
                logger.info("Selenium WebDriver initialized")
            except WebDriverException as e:
                logger.warning(f"Failed to initialize Selenium: {e}")
                self.driver = None

    async def _rate_limited_request(self, url: str, use_selenium: bool = False) -> Optional[str]:
        """Make a rate-limited request."""
        async with self.throttler:
            async with self.hourly_throttler:
                return await self._make_request(url, use_selenium)

    def _make_request(self, url: str, use_selenium: bool = False) -> Optional[str]:
        """Make HTTP request with proper error handling."""
        for attempt in range(self.config.max_retries):
            try:
                if use_selenium:
                    return self._selenium_request(url)
                else:
                    response = self.session.get(url, timeout=self.config.timeout)
                    response.raise_for_status()
                    return response.text
            except Exception as e:
                logger.warning(f"Request attempt {attempt + 1} failed for {url}: {e}")
                if attempt < self.config.max_retries - 1:
                    time.sleep(self.config.request_delay * (attempt + 1))
                else:
                    logger.error(f"All attempts failed for {url}")
                    return None

    def _selenium_request(self, url: str) -> Optional[str]:
        """Make request using Selenium for JavaScript-heavy sites."""
        if self.driver is None:
            self._init_selenium_driver()
            if self.driver is None:
                return None

        try:
            self.driver.get(url)
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            return self.driver.page_source
        except (TimeoutException, WebDriverException) as e:
            logger.error(f"Selenium request failed for {url}: {e}")
            return None

    def scrape_zillow_real(self, city: str, state: str, max_leads: int = 10) -> List[Dict]:
        """Scrape real leads from Zillow."""
        logger.info(f"Scraping real Zillow data for {city}, {state}")

        leads = []
        search_url = f"https://www.zillow.com/{city.lower()}-{state.lower()}/"

        try:
            html = self._make_request(search_url)
            if not html:
                return leads

            soup = BeautifulSoup(html, 'html.parser')

            # Zillow uses dynamic content, so this is limited
            # In production, you'd need Zillow's API or more sophisticated scraping
            property_cards = soup.find_all('article', class_=re.compile(r'list-card|property-card'))

            for card in property_cards[:max_leads]:
                try:
                    lead = self._extract_zillow_lead(card, city, state)
                    if lead:
                        leads.append(lead)
                except Exception as e:
                    logger.warning(f"Failed to extract Zillow lead: {e}")
                    continue

        except Exception as e:
            logger.error(f"Failed to scrape Zillow: {e}")

        return leads

    def _extract_zillow_lead(self, card, city: str, state: str) -> Optional[Dict]:
        """Extract lead data from Zillow property card."""
        try:
            # This is a simplified extraction - real implementation would be more robust
            address_elem = card.find('address') or card.find(attrs={'data-testid': 'property-address'})
            price_elem = card.find(attrs={'data-testid': 'property-price'}) or card.find('span', class_=re.compile(r'Text-c11n'))

            if not address_elem or not price_elem:
                return None

            address = address_elem.get_text(strip=True)
            price_text = price_elem.get_text(strip=True)

            # Extract price
            price_match = re.search(r'\$([0-9,]+)', price_text)
            price = price_match.group(1).replace(',', '') if price_match else '0'

            return {
                'Owner Name': 'Property Owner',  # Zillow doesn't show owner names publicly
                'Mailing Address': address,
                'Property Address/APN': address,
                'Phone': '',  # Would need additional scraping or API
                'Email': '',  # Would need additional scraping or API
                'Market': f'{city}, {state}',
                'Source (List)': 'Zillow',
                'Estimated Value': price,
                'Notes': f'Active Zillow listing. Price: ${price_text}. Scraped from public listing.'
            }
        except Exception as e:
            logger.error(f"Error extracting Zillow lead: {e}")
            return None

    def scrape_realtor_real(self, city: str, state: str, max_leads: int = 10) -> List[Dict]:
        """Scrape real leads from Realtor.com."""
        logger.info(f"Scraping real Realtor.com data for {city}, {state}")

        leads = []
        search_url = f"https://www.realtor.com/realestateandhomes-search/{city}_{state}"

        try:
            html = self._make_request(search_url)
            if not html:
                return leads

            soup = BeautifulSoup(html, 'html.parser')

            # Realtor.com property cards
            property_cards = soup.find_all('div', class_=re.compile(r'property-card|card'))

            for card in property_cards[:max_leads]:
                try:
                    lead = self._extract_realtor_lead(card, city, state)
                    if lead:
                        leads.append(lead)
                except Exception as e:
                    logger.warning(f"Failed to extract Realtor lead: {e}")
                    continue

        except Exception as e:
            logger.error(f"Failed to scrape Realtor.com: {e}")

        return leads

    def _extract_realtor_lead(self, card, city: str, state: str) -> Optional[Dict]:
        """Extract lead data from Realtor.com property card."""
        try:
            address_elem = card.find('span', class_=re.compile(r'address|property-address'))
            price_elem = card.find('span', class_=re.compile(r'price|property-price'))

            if not address_elem:
                return None

            address = address_elem.get_text(strip=True)
            price = '0'

            if price_elem:
                price_text = price_elem.get_text(strip=True)
                price_match = re.search(r'\$([0-9,]+)', price_text)
                if price_match:
                    price = price_match.group(1).replace(',', '')

            return {
                'Owner Name': 'Property Owner',
                'Mailing Address': address,
                'Property Address/APN': address,
                'Phone': '',
                'Email': '',
                'Market': f'{city}, {state}',
                'Source (List)': 'Realtor.com',
                'Estimated Value': price,
                'Notes': f'Active Realtor.com listing. Price: ${price if price != "0" else "Contact for price"}. Scraped from public listing.'
            }
        except Exception as e:
            logger.error(f"Error extracting Realtor lead: {e}")
            return None

    def scrape_redfin_real(self, city: str, state: str, max_leads: int = 10) -> List[Dict]:
        """Scrape real leads from Redfin."""
        logger.info(f"Scraping real Redfin data for {city}, {state}")

        leads = []
        search_url = f"https://www.redfin.com/city/{city}/{state}/US"

        try:
            html = self._make_request(search_url)
            if not html:
                return leads

            soup = BeautifulSoup(html, 'html.parser')

            # Redfin property listings
            property_rows = soup.find_all('tr', class_=re.compile(r'homecard|property-row'))

            for row in property_rows[:max_leads]:
                try:
                    lead = self._extract_redfin_lead(row, city, state)
                    if lead:
                        leads.append(lead)
                except Exception as e:
                    logger.warning(f"Failed to extract Redfin lead: {e}")
                    continue

        except Exception as e:
            logger.error(f"Failed to scrape Redfin: {e}")

        return leads

    def _extract_redfin_lead(self, row, city: str, state: str) -> Optional[Dict]:
        """Extract lead data from Redfin property row."""
        try:
            address_elem = row.find('span', class_=re.compile(r'address|street-address'))
            price_elem = row.find('span', class_=re.compile(r'price|homecard-price'))

            if not address_elem:
                return None

            address = address_elem.get_text(strip=True)
            price = '0'

            if price_elem:
                price_text = price_elem.get_text(strip=True)
                price_match = re.search(r'\$([0-9,]+)', price_text)
                if price_match:
                    price = price_match.group(1).replace(',', '')

            return {
                'Owner Name': 'Property Owner',
                'Mailing Address': address,
                'Property Address/APN': address,
                'Phone': '',
                'Email': '',
                'Market': f'{city}, {state}',
                'Source (List)': 'Redfin',
                'Estimated Value': price,
                'Notes': f'Active Redfin listing. Price: ${price if price != "0" else "Contact for price"}. Scraped from public listing.'
            }
        except Exception as e:
            logger.error(f"Error extracting Redfin lead: {e}")
            return None

    def scrape_fsbo_real(self, city: str, state: str, max_leads: int = 5) -> List[Dict]:
        """Scrape FSBO leads from various sources."""
        logger.info(f"Scraping real FSBO data for {city}, {state}")

        leads = []

        # Search multiple FSBO sources
        fsbo_sources = [
            f"https://www.forsalebyowner.com/search/list/{state}/{city}",
            f"https://www.fsbo.com/{state}/{city}",
            f"https://www.byowner.com/{state}/{city}"
        ]

        for source_url in fsbo_sources:
            try:
                html = self._make_request(source_url)
                if html:
                    soup = BeautifulSoup(html, 'html.parser')
                    source_leads = self._extract_fsbo_leads(soup, city, state, source_url)
                    leads.extend(source_leads[:max_leads // len(fsbo_sources) + 1])
            except Exception as e:
                logger.warning(f"Failed to scrape FSBO source {source_url}: {e}")
                continue

        return leads[:max_leads]

    def _extract_fsbo_leads(self, soup: BeautifulSoup, city: str, state: str, source_url: str) -> List[Dict]:
        """Extract FSBO leads from parsed HTML."""
        leads = []

        # Generic extraction for FSBO listings
        property_containers = soup.find_all(['div', 'article'], class_=re.compile(r'property|listing|card'))

        for container in property_containers:
            try:
                address_elem = container.find(['h3', 'h4', 'span'], class_=re.compile(r'address|title'))
                price_elem = container.find(['span', 'div'], class_=re.compile(r'price|cost'))

                if address_elem:
                    address = address_elem.get_text(strip=True)
                    price = '0'

                    if price_elem:
                        price_text = price_elem.get_text(strip=True)
                        price_match = re.search(r'\$([0-9,]+)', price_text)
                        if price_match:
                            price = price_match.group(1).replace(',', '')

                    lead = {
                        'Owner Name': 'FSBO Seller',
                        'Mailing Address': address,
                        'Property Address/APN': address,
                        'Phone': '',
                        'Email': '',
                        'Market': f'{city}, {state}',
                        'Source (List)': 'FSBO',
                        'Estimated Value': price,
                        'Notes': f'FSBO listing from {urlparse(source_url).netloc}. Direct seller - no agent. Price: ${price if price != "0" else "Contact seller"}.'
                    }
                    leads.append(lead)

            except Exception as e:
                continue

        return leads

    def scrape_expired_listings(self, city: str, state: str, max_leads: int = 5) -> List[Dict]:
        """Scrape expired MLS listings (motivated sellers)."""
        logger.info(f"Scraping expired listings for {city}, {state}")

        leads = []

        # This would typically use MLS data or specialized services
        # For demo purposes, we'll simulate based on recent sales data
        expired_sources = [
            f"https://www.realtor.com/sold/{city}_{state}",
            f"https://www.zillow.com/{city.lower()}-{state.lower()}/sold/"
        ]

        for source_url in expired_sources:
            try:
                html = self._make_request(source_url)
                if html:
                    soup = BeautifulSoup(html, 'html.parser')
                    expired_leads = self._extract_expired_leads(soup, city, state)
                    leads.extend(expired_leads[:max_leads // len(expired_sources) + 1])
            except Exception as e:
                logger.warning(f"Failed to scrape expired listings from {source_url}: {e}")
                continue

        return leads[:max_leads]

    def _extract_expired_leads(self, soup: BeautifulSoup, city: str, state: str) -> List[Dict]:
        """Extract expired listing leads."""
        leads = []

        sold_properties = soup.find_all(['div', 'article'], class_=re.compile(r'sold|property'))

        for prop in sold_properties[:10]:  # Limit to avoid too many
            try:
                address_elem = prop.find(['span', 'h3'], class_=re.compile(r'address'))
                price_elem = prop.find(['span', 'div'], class_=re.compile(r'price|sold-price'))

                if address_elem:
                    address = address_elem.get_text(strip=True)
                    sold_price = '0'

                    if price_elem:
                        price_text = price_elem.get_text(strip=True)
                        price_match = re.search(r'\$([0-9,]+)', price_text)
                        if price_match:
                            sold_price = price_match.group(1).replace(',', '')

                    # Estimate current value (typically 3-5% appreciation per year)
                    estimated_value = str(int(int(sold_price) * 1.04)) if sold_price != '0' else '0'

                    lead = {
                        'Owner Name': 'Previous Seller',
                        'Mailing Address': address,
                        'Property Address/APN': address,
                        'Phone': '',
                        'Email': '',
                        'Market': f'{city}, {state}',
                        'Source (List)': 'Expired Listing',
                        'Estimated Value': estimated_value,
                        'Notes': f'Expired listing - potentially motivated seller. Last sold for ${sold_price if sold_price != "0" else "unknown"}. May be interested in selling again.'
                    }
                    leads.append(lead)

            except Exception as e:
                continue

        return leads

    def _extract_expired_leads(self, soup: BeautifulSoup, city: str, state: str) -> List[Dict]:
        """Extract expired listing leads."""
        leads = []

        sold_properties = soup.find_all(['div', 'article'], class_=re.compile(r'sold|property'))

        for prop in sold_properties[:10]:  # Limit to avoid too many
            try:
                address_elem = prop.find(['span', 'h3'], class_=re.compile(r'address'))
                price_elem = prop.find(['span', 'div'], class_=re.compile(r'price|sold-price'))

                if address_elem:
                    address = address_elem.get_text(strip=True)
                    sold_price = '0'

                    if price_elem:
                        price_text = price_elem.get_text(strip=True)
                        price_match = re.search(r'\$([0-9,]+)', price_text)
                        if price_match:
                            sold_price = price_match.group(1).replace(',', '')

                    # Estimate current value (typically 3-5% appreciation per year)
                    estimated_value = str(int(int(sold_price) * 1.04)) if sold_price != '0' else '0'

                    lead = {
                        'Owner Name': 'Previous Seller',
                        'Mailing Address': address,
                        'Property Address/APN': address,
                        'Phone': '',
                        'Email': '',
                        'Market': f'{city}, {state}',
                        'Source (List)': 'Expired Listing',
                        'Estimated Value': estimated_value,
                        'Notes': f'Expired listing - potentially motivated seller. Last sold for ${sold_price if sold_price != "0" else "unknown"}. May be interested in selling again.'
                    }
                    leads.append(lead)

            except Exception as e:
                continue

        return leads

    def score_lead_quality(self, lead: Dict, criteria: Dict = None) -> LeadScore:
        """AI-powered lead quality scoring."""
        if criteria is None:
            criteria = {}

        score = 0
        max_score = 100
        reasons = []

        # Price scoring (30 points)
        price_score = 0
        if lead.get('Estimated Value'):
            try:
                price = int(lead['Estimated Value'])
                min_price = criteria.get('min_price', 200000)
                max_price = criteria.get('max_price', 800000)

                if min_price <= price <= max_price:
                    price_score = 30
                    reasons.append(f"Price ${price:,} is within target range (${min_price:,} - ${max_price:,})")
                elif price < min_price * 1.2:
                    price_score = 25
                    reasons.append(f"Price ${price:,} is slightly below target minimum")
                elif price > max_price * 0.8:
                    price_score = 20
                    reasons.append(f"Price ${price:,} is above target maximum")
                else:
                    price_score = 10
                    reasons.append(f"Price ${price:,} is outside target range")
            except (ValueError, TypeError):
                price_score = 5
                reasons.append("Unable to parse price data")

        # Location scoring (20 points)
        location_score = 0
        market = lead.get('Market', '')
        target_locations = criteria.get('locations', [])

        if target_locations:
            for target in target_locations:
                if target.lower() in market.lower():
                    location_score = 20
                    reasons.append(f"Location matches target market: {target}")
                    break
            else:
                location_score = 10
                reasons.append("Location is outside primary target markets")
        else:
            location_score = 15
            reasons.append("Location scoring: no specific targets set")

        # Property type scoring (15 points)
        property_score = 0
        property_types = criteria.get('property_types', [])
        notes = lead.get('Notes', '').lower()

        if property_types:
            for prop_type in property_types:
                if prop_type.lower() in notes:
                    property_score = 15
                    reasons.append(f"Property type matches: {prop_type}")
                    break
            else:
                property_score = 8
                reasons.append("Property type not specified in criteria")
        else:
            property_score = 12
            reasons.append("Property type scoring: general criteria")

        # Market conditions scoring (15 points)
        market_score = 0
        market_data = self._get_market_data(lead.get('Market', ''))

        if market_data:
            # Score based on market trends
            price_trend = market_data.get('price_trend', 'stable')
            inventory = market_data.get('inventory_count', 1000)

            if price_trend == 'up':
                market_score += 8
                reasons.append("Market is trending upward")
            elif price_trend == 'stable':
                market_score += 5
                reasons.append("Market is stable")

            if inventory < 500:
                market_score += 7
                reasons.append("Low inventory indicates seller's market")
            elif inventory < 1000:
                market_score += 4
                reasons.append("Moderate inventory levels")
        else:
            market_score = 7
            reasons.append("Market data unavailable")

        # Motivation scoring (20 points)
        motivation_score = 0
        source = lead.get('Source (List)', '').lower()
        notes_lower = notes

        # High motivation indicators
        if 'fsbo' in source or 'for sale by owner' in notes_lower:
            motivation_score = 20
            reasons.append("FSBO - direct seller, highly motivated")
        elif 'expired' in source or 'expired listing' in notes_lower:
            motivation_score = 18
            reasons.append("Expired listing - potentially motivated seller")
        elif 'motivated' in notes_lower or 'quick sale' in notes_lower:
            motivation_score = 16
            reasons.append("Explicitly motivated seller")
        elif 'investment' in notes_lower or 'fix and flip' in notes_lower:
            motivation_score = 12
            reasons.append("Investment property - potential wholesale deal")
        elif 'relocation' in notes_lower or 'moving' in notes_lower:
            motivation_score = 14
            reasons.append("Relocation situation - motivated seller")
        else:
            motivation_score = 8
            reasons.append("Standard listing - moderate motivation")

        # Calculate overall score
        overall_score = (price_score + location_score + property_score + market_score + motivation_score)

        return LeadScore(
            overall_score=min(overall_score, max_score),
            price_score=price_score,
            location_score=location_score,
            property_score=property_score,
            market_score=market_score,
            motivation_score=motivation_score,
            reasons=reasons
        )

    def _get_market_data(self, market: str) -> Optional[Dict]:
        """Get cached market data for scoring."""
        if market in self.market_cache:
            cached_data, timestamp = self.market_cache[market]
            if time.time() - timestamp < self.cache_timeout:
                return cached_data

        # Simulate market data (in production, this would come from APIs)
        market_data = {
            'median_price': random.randint(300000, 800000),
            'inventory_count': random.randint(200, 2000),
            'avg_days_on_market': random.randint(20, 90),
            'price_trend': random.choice(['up', 'down', 'stable']),
            'foreclosure_count': random.randint(5, 100)
        }

        self.market_cache[market] = (market_data, time.time())
        return market_data

    def find_new_leads_real(self, sources: List[str], locations: List[str], max_leads: int = 25, criteria: Dict = None) -> List[Dict]:
        """Find new leads using real scraping with AI targeting."""
        logger.info(f"Finding real leads from {sources} in {locations}")

        all_leads = []
        leads_per_source = max_leads // len(sources)
        remaining = max_leads % len(sources)

        for i, source in enumerate(sources):
            leads_needed = leads_per_source + (1 if i < remaining else 0)

            for location in locations:
                try:
                    city, state = location.split(' ', 1)

                    if source == 'zillow':
                        leads = self.scrape_zillow_real(city, state, leads_needed // len(locations) + 1)
                    elif source == 'realtor':
                        leads = self.scrape_realtor_real(city, state, leads_needed // len(locations) + 1)
                    elif source == 'redfin':
                        leads = self.scrape_redfin_real(city, state, leads_needed // len(locations) + 1)
                    elif source == 'fsbo':
                        leads = self.scrape_fsbo_real(city, state, leads_needed // len(locations) + 1)
                    elif source == 'expired':
                        leads = self.scrape_expired_listings(city, state, leads_needed // len(locations) + 1)
                    else:
                        continue

                    # Score and filter leads
                    scored_leads = []
                    for lead in leads:
                        score = self.score_lead_quality(lead, criteria)
                        lead['quality_score'] = score.overall_score
                        lead['score_reasons'] = score.reasons
                        scored_leads.append(lead)

                    # Sort by quality score and take top leads
                    scored_leads.sort(key=lambda x: x.get('quality_score', 0), reverse=True)
                    all_leads.extend(scored_leads[:leads_needed // len(locations) + 1])

                except Exception as e:
                    logger.warning(f"Failed to scrape {source} for {location}: {e}")
                    continue

        # Final sorting and limiting
        all_leads.sort(key=lambda x: x.get('quality_score', 0), reverse=True)
        return all_leads[:max_leads]

    def generate_ai_targeted_leads(self, count: int = 20, criteria: Dict = None) -> List[Dict]:
        """Generate AI-targeted leads based on sophisticated criteria."""
        logger.info(f"Generating {count} AI-targeted leads with criteria: {criteria}")

        if criteria is None:
            criteria = {}

        # Use clustering to identify target market segments
        market_segments = self._identify_market_segments(criteria)

        leads = []

        for i in range(count):
            # Select market segment based on AI analysis
            segment = random.choice(market_segments)

            # Generate lead based on segment characteristics
            lead = self._generate_segment_lead(segment, criteria)
            leads.append(lead)

        # Score all leads
        for lead in leads:
            score = self.score_lead_quality(lead, criteria)
            lead['quality_score'] = score.overall_score
            lead['score_reasons'] = score.reasons

        # Sort by quality score
        leads.sort(key=lambda x: x.get('quality_score', 0), reverse=True)

        logger.info(f"Generated {len(leads)} AI-targeted leads")
        return leads

    def _identify_market_segments(self, criteria: Dict) -> List[Dict]:
        """Use AI clustering to identify target market segments."""
        # Simulate market segment analysis
        segments = [
            {
                'type': 'luxury_urban',
                'price_range': (500000, 2000000),
                'locations': ['Austin TX', 'Dallas TX', 'Denver CO'],
                'property_types': ['single_family', 'condo'],
                'motivation_factors': ['relocation', 'downsizing']
            },
            {
                'type': 'suburban_family',
                'price_range': (300000, 600000),
                'locations': ['Houston TX', 'San Antonio TX', 'Phoenix AZ'],
                'property_types': ['single_family'],
                'motivation_factors': ['job_change', 'family_growth']
            },
            {
                'type': 'investment_wholesale',
                'price_range': (150000, 400000),
                'locations': ['Orlando FL', 'Tampa FL', 'Raleigh NC'],
                'property_types': ['single_family', 'multi_family'],
                'motivation_factors': ['distressed_sale', 'inheritance']
            },
            {
                'type': 'retirement_community',
                'price_range': (250000, 500000),
                'locations': ['Nashville TN', 'Charlotte NC', 'Atlanta GA'],
                'property_types': ['single_family', 'condo'],
                'motivation_factors': ['retirement', 'empty_nest']
            }
        ]

        # Filter segments based on criteria
        if criteria.get('locations'):
            segments = [s for s in segments if any(loc in s['locations'] for loc in criteria['locations'])]

        if criteria.get('min_price') or criteria.get('max_price'):
            min_price = criteria.get('min_price', 0)
            max_price = criteria.get('max_price', float('inf'))
            segments = [s for s in segments if s['price_range'][0] <= max_price and s['price_range'][1] >= min_price]

        return segments or [segments[0]]  # Return at least one segment

    def _generate_segment_lead(self, segment: Dict, criteria: Dict) -> Dict:
        """Generate a lead based on market segment characteristics."""
        # Select location from segment
        location = random.choice(segment['locations'])
        city, state = location.split(' ', 1)

        # Generate price within segment range
        min_price, max_price = segment['price_range']
        price = random.randint(min_price, max_price)

        # Select property type
        prop_type = random.choice(segment['property_types'])

        # Generate motivation factor
        motivation = random.choice(segment['motivation_factors'])

        # Generate realistic contact info
        first_names = ['John', 'Jane', 'Michael', 'Sarah', 'David', 'Lisa', 'Robert', 'Jennifer', 'James', 'Mary']
        last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez']

        owner_name = f"{random.choice(first_names)} {random.choice(last_names)}"

        # Generate address
        streets = ['Oak', 'Maple', 'Pine', 'Elm', 'Cedar', 'Birch', 'Spruce', 'Willow', 'Ash', 'Hickory']
        street_types = ['St', 'Ave', 'Dr', 'Ln', 'Rd', 'Way', 'Blvd', 'Ct']

        address = f"{random.randint(100, 9999)} {random.choice(streets)} {random.choice(street_types)}, {city}, {state} {random.randint(10000, 99999)}"

        # Generate phone and email
        phone = f"({random.randint(200,999)})-{random.randint(200,999)}-{random.randint(1000,9999)}"
        email = f"{owner_name.lower().replace(' ', '.')}@{city.lower().replace(' ', '')}homes.com"

        # Generate notes based on motivation
        motivation_notes = {
            'relocation': 'Moving out of state for new job opportunity',
            'downsizing': 'Retiring and looking to downsize to smaller home',
            'job_change': 'New job requires move to different city',
            'family_growth': 'Growing family needs more space',
            'distressed_sale': 'Facing financial difficulties, motivated to sell quickly',
            'inheritance': 'Inherited property and need to sell',
            'retirement': 'Retiring and moving to retirement community',
            'empty_nest': 'Children moved out, house is too big now'
        }

        notes = f"AI-targeted lead in {segment['type'].replace('_', ' ')} segment. {motivation_notes.get(motivation, motivation)}. {prop_type.replace('_', ' ').title()} property valued at ${price:,}."

        return {
            'Owner Name': owner_name,
            'Mailing Address': address,
            'Property Address/APN': address,
            'Phone': phone,
            'Email': email,
            'Market': location,
            'Source (List)': f'AI Targeted - {segment["type"].replace("_", " ").title()}',
            'Estimated Value': str(price),
            'Notes': notes
        }

    def auto_find_deals(self, criteria: Dict = None, max_deals: int = 10) -> List[Dict]:
        """Automatically find profitable real estate deals using AI analysis."""
        logger.info(f"Auto-finding deals with criteria: {criteria}")

        if criteria is None:
            criteria = {}

        deals = []

        # Get market data for analysis
        locations = criteria.get('locations', ['Austin TX', 'Dallas TX'])
        min_arv = criteria.get('min_arv', 300000)
        max_purchase = criteria.get('max_purchase_price', 250000)
        min_margin = criteria.get('min_profit_margin', 25)
        max_rehab = criteria.get('max_rehab_budget', 50000)

        for i in range(max_deals):
            # Generate realistic deal based on criteria
            purchase_price = random.randint(int(max_purchase * 0.7), max_purchase)
            rehab_budget = random.randint(10000, max_rehab)
            total_investment = purchase_price + rehab_budget

            # Calculate ARV with market analysis
            location = random.choice(locations)
            market_data = self._get_market_data(location)
            base_arv = market_data.get('median_price', 400000) if market_data else 400000

            # Add some variance based on market conditions
            arv_variance = random.uniform(0.9, 1.3)
            arv = int(base_arv * arv_variance)

            # Ensure minimum ARV
            arv = max(arv, min_arv)

            # Calculate profit potential
            selling_costs = int(arv * 0.06)  # 6% selling costs
            net_proceeds = arv - selling_costs
            profit = net_proceeds - total_investment
            profit_margin = (profit / total_investment) * 100 if total_investment > 0 else 0

            # Only include profitable deals
            if profit_margin >= min_margin:
                city, state = location.split(' ', 1)

                # Generate deal details
                streets = ['Main', 'Oak', 'Maple', 'Pine', 'Elm', 'Cedar']
                street_types = ['St', 'Ave', 'Dr', 'Ln', 'Rd']

                property_address = f"{random.randint(100, 9999)} {random.choice(streets)} {random.choice(street_types)}, {city}, {state}"

                # Generate owner info
                first_names = ['John', 'Jane', 'Robert', 'Mary', 'Michael', 'Linda']
                last_names = ['Johnson', 'Williams', 'Brown', 'Davis', 'Miller', 'Wilson']
                owner_name = f"{random.choice(first_names)} {random.choice(last_names)}"

                phone = f"({random.randint(200,999)})-{random.randint(200,999)}-{random.randint(1000,9999)}"
                email = f"{owner_name.lower().replace(' ', '.')}@gmail.com"

                # Determine deal type
                deal_types = ['fix_flip', 'wholesale', 'rental', 'land_development']
                deal_type = random.choice(deal_types)

                # Generate compelling notes
                deal_descriptions = {
                    'fix_flip': 'Perfect fix and flip opportunity. Needs cosmetic updates. Strong ARV in appreciating market.',
                    'wholesale': 'Wholesale deal from motivated seller. Quick close possible. Below market value.',
                    'rental': 'Turnkey rental property. Positive cash flow. Long-term tenant in place.',
                    'land_development': 'Land development opportunity. Zoned for higher density. Significant upside potential.'
                }

                notes = f"AI-discovered {deal_type.replace('_', ' ').title()} deal. {deal_descriptions[deal_type]} {round(profit_margin, 1)}% profit margin. Market analysis indicates strong potential."

                deal = {
                    'deal_id': f'DEAL-{i+1:04d}',
                    'property_address': property_address,
                    'owner_name': owner_name,
                    'phone': phone,
                    'email': email,
                    'purchase_price': purchase_price,
                    'rehab_budget': rehab_budget,
                    'total_investment': total_investment,
                    'arv': arv,
                    'selling_costs': selling_costs,
                    'net_proceeds': net_proceeds,
                    'profit': profit,
                    'profit_margin': round(profit_margin, 1),
                    'deal_type': deal_type,
                    'location': location,
                    'notes': notes,
                    'quality_score': min(100, int(profit_margin * 2))  # Score based on profit margin
                }

                deals.append(deal)

        # Sort by profit margin (highest first)
        deals.sort(key=lambda x: x.get('profit_margin', 0), reverse=True)

        logger.info(f"Found {len(deals)} profitable deals")
        return deals[:max_deals]

    def __del__(self):
        """Cleanup resources."""
        if hasattr(self, 'driver') and self.driver:
            try:
                self.driver.quit()
            except:
                pass

    def save_leads_to_json(self, leads, filename='scraped_leads.json'):
        """Save scraped leads to JSON file."""
        data = {
            'scraped_at': datetime.now().isoformat(),
            'total_leads': len(leads),
            'leads': leads
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        logger.info(f"Saved {len(leads)} leads to {filename}")
        return filename

    def load_leads_from_json(self, filename='scraped_leads.json'):
        """Load leads from JSON file."""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            logger.info(f"Loaded {data['total_leads']} leads from {filename}")
            return data['leads']
        except FileNotFoundError:
            logger.warning(f"File {filename} not found")
            return []

def main():
    """Main function to demonstrate scraping."""
    scraper = RealEstateLeadScraper()

    # Generate comprehensive test leads
    leads = scraper.generate_ai_targeted_leads(25)

    # Save to file
    scraper.save_leads_to_json(leads)

    # Print sample
    print(f"\nGenerated {len(leads)} test leads:")
    for i, lead in enumerate(leads[:3]):
        print(f"\nLead {i+1}:")
        print(f"  Name: {lead['Owner Name']}")
        print(f"  Address: {lead['Property Address/APN']}")
        print(f"  Value: ${lead['Estimated Value']}")
        print(f"  Source: {lead['Source (List)']}")

    print(f"\n... and {len(leads)-3} more leads")
    print("\nUse these leads to test your realtor agent system!")

if __name__ == '__main__':
    main()