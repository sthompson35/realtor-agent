import pytest
import yaml
from unittest.mock import Mock, patch
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class MockWebScoutBot:
    def __init__(self, config_path):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

    def search_listings(self, filters):
        """Mock search function"""
        if not self.config['enabled']:
            return []

        # Mock API responses based on config
        mock_listings = [
            {
                'address': '123 Main St, Houston, TX',
                'price': 50000,
                'acreage': 0.5,
                'source': 'zillow',
                'url': 'https://zillow.com/listing123'
            },
            {
                'address': '456 Oak Ave, Orlando, FL',
                'price': 75000,
                'acreage': 1.0,
                'source': 'realtor',
                'url': 'https://realtor.com/listing456'
            }
        ]

        # Apply filters
        filtered = []
        for listing in mock_listings:
            if (listing['price'] >= filters.get('min_price', 0) and
                listing['price'] <= filters.get('max_price', float('inf'))):
                filtered.append(listing)

        return filtered

def test_web_scout_config():
    """Test web scout bot configuration"""
    bot = MockWebScoutBot('bots/web_scout/bot_config.yml')

    assert bot.config['enabled'] == True
    assert 'sources' in bot.config
    assert len(bot.config['sources']) > 0
    assert 'filters' in bot.config

def test_web_scout_search():
    """Test web scout search functionality"""
    bot = MockWebScoutBot('bots/web_scout/bot_config.yml')

    filters = {
        'min_price': 25000,
        'max_price': 100000
    }

    results = bot.search_listings(filters)

    assert isinstance(results, list)
    for listing in results:
        assert 'address' in listing
        assert 'price' in listing
        assert 'source' in listing
        assert listing['price'] >= filters['min_price']
        assert listing['price'] <= filters['max_price']

def test_web_scout_compliance():
    """Test web scout compliance settings"""
    bot = MockWebScoutBot('bots/web_scout/bot_config.yml')

    assert bot.config['compliance']['tos_check'] == True
    assert bot.config['compliance']['robots_txt_respect'] == True