+===============================================================================+
|                  REALTOR-AGENT SCRAPING & DEAL-FINDING ENGINE                 |
+===============================================================================+

INTERNET (target sites: .com, .org, .net, .info, etc.)
      |
      v
+----------------------------+
|  TARGET DISCOVERY LAYER    |
+----------------------------+
| - Domain filters (.com...) |
| - Vertical filters (realty)|
| - Robots / TOS checker     |
+----------------------------+
      |
      v
+----------------------------+
|  CRAWLER & FETCHER LAYER   |
+----------------------------+
| - URL queues               |
| - Rate limiting            |
| - Proxy / headers          |
| - Error retries            |
+----------------------------+
      |
      v
+----------------------------+
|  PARSING & NORMALIZATION   |
+----------------------------+
| - HTML/JSON parsers        |
| - Site-specific extractors |
| - Normalize -> schema      |
+----------------------------+
      |
      v
+----------------------------+
|  DEAL SCORING ENGINE       |
+----------------------------+
| - Property-level scores    |
| - City/zip/state scores    |
| - Trend detection          |
+----------------------------+
      |
      v
+----------------------------+
|  DEDUP / QUALITY FILTERS   |
+----------------------------+
| - Remove dup listings      |
| - Sanity checks            |
| - Missing data handling    |
+----------------------------+
      |
      v
+----------------------------+
|  DATA SINKS (LANDOS)       |
+----------------------------+
| - DATA/PROPERTIES/*.csv    |
| - DATA/MARKETS/*.csv       |
| - ANALYTICS/*_REPORT.json  |
| - CLIENTS/* leads          |
+----------------------------+
      |
      v
+----------------------------+
|  STRATEGY / UI INTEGRATION |
+----------------------------+
| - STRATEGY/MARKET_SHIFT_*  |
| - STRATEGY/LISTING_*       |
| - dashboards & alerts      |
+----------------------------+

# REALTOR-AGENT SCRAPE RULES (CANONICAL)

## 1. SCOPE

- Target TLDs: `.com`, `.org`, `.net`, `.info`, plus country TLDs where allowed.
- Target verticals:
  - Real estate listings
  - MLS-like aggregators
  - City / neighborhood data
  - Government / non-profit housing data (.gov, .org) where allowed
- Output:
  - Property-level records
  - Market-level records (city/zip/state)
  - Deal scores & rankings

---

## 2. LEGAL & ETHICAL RULES

1. **Robots.txt compliance**
   - Always check `/robots.txt`.
   - Do not scrape disallowed paths.
2. **Terms of Service**
   - Review site TOS; if scraping is forbidden, do not scrape.
3. **Rate limiting**
   - Default: max 1 request / second / domain (adjustable).
4. **No personal sensitive data**
   - Do not collect SSNs, exact DOB, financial account info, etc.
5. **Attribution**
   - If site requires attribution and data is used, follow attribution rules.

---

## 3. TARGET DISCOVERY RULES

### 3.1 Domain selection

Include if:
- Domain mentions real estate keywords:
  - `realty`, `realestate`, `homes`, `property`, `realtor`, `mls`, `housing`.
- OR is known city/market data:
  - `.gov` sites for census, housing stats.
- AND passes `robots.txt` & TOS checks.

Exclude if:
- Generic content farms not clearly providing real estate/market data.
- Obvious spam, malware, or scraper traps.

### 3.2 URL patterns (examples)

- Listing pages:
  - `/property/*`, `/listing/*`, `/homes-for-sale/*`, `/rent/*`
- Search result / map pages:
  - `/homes/*`, `/search/*`, `/real-estate/*`
- Market/city data pages:
  - `/market-trends/*`, `/housing/*`, `/city/*`, `/neighborhood/*`

---

## 4. DATA SCHEMA

### 4.1 Property-level schema

- `property_id` (hash of URL + address)
- `source_domain`
- `listing_url`
- `address_full`
- `street`, `city`, `state`, `zipcode`
- `country`
- `lat`, `lng` (if available)
- `list_price`
- `bedrooms`, `bathrooms`, `sqft`, `lot_size`, `year_built`
- `property_type` (single_family, condo, multi_family, land, etc.)
- `days_on_market`
- `status` (active, pending, sold, off_market)
- `estimated_rent` (if available or computed)
- `hoa_fee`, `property_taxes_est`
- `description_raw`
- `features` (garage, pool, view, etc.)
- `last_scraped_at`

### 4.2 Market-level schema (city/zip/state)

- `geo_level` (city, zip, county, state)
- `geo_id` (name or code)
- `median_list_price`
- `median_sold_price`
- `price_per_sqft`
- `inventory_count`
- `avg_days_on_market`
- `rental_yield_est`
- `trend_1y_price_change`
- `trend_1y_rent_change`
- `created_at`
- `source_domains` (list)

---

## 5. DEAL SCORING RULES

### 5.1 Property-level deal score

Score each property with a composite score:

- `undervaluation_score`:
  - Compare list_price vs city/zip median adjusted for sqft and bed/bath.
- `yield_score`:
  - Estimate `gross_yield = 12 * estimated_rent / list_price`.
- `liquidity_score`:
  - Neighbor DOM vs average DOM; shorter DOM markets → higher.
- `value_add_score`:
  - Keywords: "needs TLC", "fixer", "as-is", etc. (optional, risk-aware).

Overall:

`deal_score = w1*undervaluation + w2*yield + w3*liquidity + w4*value_add - penalties`

Penalties for:
- Missing critical data
- Obvious anomalies (price too low to be real, etc.)

### 5.2 Market-level opportunity score

For each city/zip/state:

- `growth_score` (price & rent trends)
- `affordability_score` (price vs income / rent levels)
- `inventory_score` (balanced, not extremely tight)
- `liquidity_score` (DOM vs national/region)

`market_score = g1*growth + g2*affordability + g3*inventory + g4*liquidity`

---

## 6. CRAWLING & PARSING RULES

1. Use **site-specific parsers** when possible:
   - For known portals, define CSS/XPath/JSON selectors explicitly.
2. Fallback to **AI-assisted parsing** for new sites:
   - Extract address, price, features, description from HTML chunks.
3. Normalize all data to the canonical schemas above.
4. Ensure `property_id` stability (same property across scrapes).

---

## 7. DEDUP & QUALITY RULES

- Deduplicate by:
  - (address_full, list_price, sqft) or stable `property_id`.
- Reject records if:
  - No address or no price.
  - Clear garbage values.
- Mark as `low_confidence` if lots of missing attributes.

---

## 8. OUTPUT / INTEGRATION RULES

### 8.1 Files in LANDOS

- `DATA/PROPERTIES/properties_raw_YYYYMMDD.csv`
- `DATA/PROPERTIES/properties_scored_YYYYMMDD.csv`
- `DATA/MARKETS/markets_scored_YYYYMMDD.csv`
- `ANALYTICS/BEST_DEALS_REPORT.json`
- `ANALYTICS/BEST_MARKETS_REPORT.json`

### 8.2 Connection to REALTOR_AGENT_SYSTEM

- Feed scored properties into:
  - `LEAD_GENERATION_MODULE` (targeted prospecting areas)
  - `LISTING_MODULE` (fsbo/expired/probable seller targeting)
- Feed market scores into:
  - `MARKET_SHIFT_STRATEGY.md`
  - `ANNUAL_STRATEGY.md` (where to focus expansion)

---

## 9. SCHEDULING

- Property scrape:
  - Daily or multiple times/day for hot markets.
- Market stats:
  - Daily or weekly, depending on data freshness.
- Re-score deals whenever new prices or rents appear.

# scrape_config.yaml

domains:
  allowed_tlds: [".com", ".org", ".net", ".info"]
  keywords:
    include: ["realestate", "realty", "homes", "property", "mls", "housing"]
  respect_robots: true
  max_requests_per_second_per_domain: 1

targets:
  - name: generic_listing_pages
    url_patterns:
      - "/property/"
      - "/listing/"
      - "/homes-for-sale/"
      - "/real-estate/"
    parse:
      type: "ai_or_rule_based"
      property_schema:
        id: "hash(url + address)"
        fields:
          address: ["meta[property='og:street-address']", ".address", "//*[contains(@class,'address')]"]
          city: [".city", "//*[contains(@class,'city')]"]
          state: [".state", "//*[contains(@class,'state')]"]
          zipcode: [".zip", "//*[contains(@class,'zip')]", "//*[contains(text(),'ZIP')]"]
          price: [".price", "//*[contains(@class,'price')]"]
          beds: [".beds", "//*[contains(@class,'beds')]"]
          baths: [".baths", "//*[contains(@class,'baths')]"]
          sqft: [".sqft", "//*[contains(@class,'sqft')]"]
          description: [".description", "//*[contains(@class,'description')]"]
    output:
      file: "DATA/PROPERTIES/properties_raw_{{date}}.csv"

scoring:
  property:
    weights:
      undervaluation: 0.4
      yield: 0.3
      liquidity: 0.2
      value_add: 0.1
    penalties:
      missing_critical: 0.3
      anomalous_price: 0.5
  market:
    weights:
      growth: 0.3
      affordability: 0.3
      inventory: 0.2
      liquidity: 0.2

output:
  best_deals:
    file: "ANALYTICS/BEST_DEALS_REPORT.json"
    top_n: 100
  best_markets:
    file: "ANALYTICS/BEST_MARKETS_REPORT.json"
    top_n: 50

  +================================================================================+
|                 GLOBAL REALTOR-AGENT DEAL DISCOVERY ENGINE                     |
+================================================================================+

  INTERNET (.com, .org, .net, .info, .gov, ccTLDs)          MACRO LAYERS
          |                                                 ------------
          v
+------------------------+        +--------------------+    Region/Strategy
|  COUNTRY/GEO FILTER    |<------>| STRATEGY PROFILE   |    filters: US+Globe,
+------------------------+        +--------------------+    buy&hold / flip / OO
          |
          v
+------------------------+
|   TARGET DISCOVERY     |  (.com, .org, .net, .info, ccTLDs)
+------------------------+
          |
          v
+------------------------+        +--------------------+
| CRAWLER & FETCHER      |-----> | REQUEST SCHEDULER  | (US = higher freq)
+------------------------+        +--------------------+
          |
          v
+------------------------+
| PARSER & NORMALIZER    |  (site-specific + AI parsers)
+------------------------+
          |
          v
+------------------------+
| DEAL SCORING ENGINE    |  (per property + per market, by strategy)
+------------------------+
          |
          v
+------------------------+
| DEDUP & QUALITY FILTER |
+------------------------+
          |
          v
+------------------------+
| LANDOS SINKS           |  (DATA/, ANALYTICS/, STRATEGY/)
+------------------------+
          |
          v
+------------------------+
| REALTOR_AGENT_SYSTEM   |  (LeadGen, Listings, Strategy, UI)
+------------------------+  

Strategy-Aware Data Schema
3.1 Property-level (enhanced)
Add strategy fields and global geo:

property_id
source_domain
listing_url
address_full
street, city, state_region, zipcode_postcode
country_code (ISO-2; e.g., US, CA, GB, DE, AU)
lat, lng
list_price
currency (USD, EUR, GBP, etc.)
bedrooms, bathrooms, sqft, lot_size, year_built
property_type (single_family, condo, multi_family, land, mixed_use, etc.)
status (active, pending, sold, off_market)
days_on_market
Rent/yield fields:
estimated_rent_monthly_local
estimated_rent_source (site, model, manual)
gross_yield_est (standardized in USD or local currency)
Condition / value-add fields:
condition_est (excellent/good/fair/poor/tear_down)
needs_renovation (bool)
renovation_keywords (from description: “as-is”, “TLC”, “fixer”, etc.)
Strategy tags (multi-select):
strategy_tags: list like:
["buy_and_hold"]
["fix_and_flip"]
["owner_occupant"]
["buy_and_hold", "owner_occupant"]
These come from:
Property type
Price range vs incomes
Local rent/price
Condition keywords
last_scraped_at
3.2 Market-level (city/zip/neighborhood/state/country)
geo_level (neighborhood, zip, city, county, state_region, country)
geo_id (e.g., “US-TX-Austin”, “GB-London”, “DE-Berlin”)
country_code
Core stats:
median_list_price
median_sold_price
median_rent_monthly
price_per_sqft
inventory_count
avg_days_on_market
Trend metrics:
price_change_1y_pct
rent_change_1y_pct
inventory_change_1y_pct
dom_change_1y_pct
Strategy scores (0–100) per style:
score_buy_and_hold
score_fix_and_flip
score_owner_occupant
created_at
source_domains
4. Strategy-Specific Deal Scoring
We’ll implement three partial scores per property and pick or combine depending on your use.

4.1 For Buy & Hold Rentals
Focus on yield + stability:

yield_score:
High gross_yield_est ⇒ high score
stability_score:
Lower price volatility & stable/positive rent trend
tenant_demand_score:
Short DOM, low vacancy proxies (inventory + time to rent if available)
landlord_friendliness_score (US-only where possible):
Very rough: state/city known landlord/tenant laws → config

buy_and_hold_score =
  0.45 * normalized(gross_yield_est)
+ 0.25 * normalized(stability_score)
+ 0.20 * normalized(tenant_demand_score)
+ 0.10 * normalized(landlord_friendliness_score)

4.2 For Fix & Flip
Focus on spread + velocity:

discount_score:
List price vs estimated ARV (from comps)
renovation_potential_score:
Condition keywords, age, photos (if parseable)
velocity_score:
DOM vs average; strong liquidity = faster exit
risk_penalty:
Very long DOM, high crime proxies (if any), unstable markets

fix_and_flip_score =
  0.50 * normalized(discount_score)
+ 0.25 * normalized(renovation_potential_score)
+ 0.20 * normalized(velocity_score)
- 0.15 * normalized(risk_penalty)

4.3 For Owner-Occupant
Focus on livability + stability:

affordability_score:
Price vs median income (market-level; approximate)
stability_score:
Low volatility, moderate price growth (no extreme bubble signature)
quality_of_life_proxy:
School ratings, crime, amenities (where data exists; otherwise neutral)
liquidity_score:
Reasonable DOM; easier resale potential

owner_occupant_score =
  0.35 * normalized(affordability_score)
+ 0.25 * normalized(stability_score)
+ 0.25 * normalized(quality_of_life_proxy)
+ 0.15 * normalized(liquidity_score)

Each property ends up with:

deal_score_buy_and_hold
deal_score_fix_and_flip
deal_score_owner_occupant
and a combined:

deal_score_combined = max(
  deal_score_buy_and_hold,
  deal_score_fix_and_flip,
  deal_score_owner_occupant
)

5. Region-Aware Rules
5.1 US (Tier 1)
Frequency:
Property scrape: multiple times per day in top metro areas
Market stats: daily
Extra signals:
State-specific:
Landlord/tenant friendliness (config map)
Property tax characteristics by state/county
MSA/county-level:
Job growth, population growth (where accessible from open data)
File outputs (US-specific):

DATA/PROPERTIES/us_properties_raw_YYYYMMDD.csv
DATA/PROPERTIES/us_properties_scored_YYYYMMDD.csv
DATA/MARKETS/us_markets_scored_YYYYMMDD.csv
ANALYTICS/US_BEST_DEALS_REPORT.json
ANALYTICS/US_BEST_MARKETS_REPORT.json

5.2 Global (Tier 2)
Frequency:
Property scrape: daily or a few times per week
Market stats: weekly
Extra handling:
Currency normalization:
Convert to USD (or base) via FX rates table.
Region config:
Certain metrics simply won’t exist in many markets; mark as null and avoid over-penalizing.
File outputs (global):

DATA/PROPERTIES/global_properties_raw_YYYYMMDD.csv
DATA/PROPERTIES/global_properties_scored_YYYYMMDD.csv
DATA/MARKETS/global_markets_scored_YYYYMMDD.csv
ANALYTICS/GLOBAL_BEST_DEALS_REPORT.json
ANALYTICS/GLOBAL_BEST_MARKETS_REPORT.json

Updated scrape_rules.md Template (ready-to-use)
You can embed the above ideas like this:

# REALTOR-AGENT GLOBAL SCRAPE RULES

## 1. REGIONS

- Tier 1 (US – High Frequency)
- Tier 2 (Global – Medium Frequency)
  - Canada, UK, Western Europe, AU/NZ, select emerging markets

## 2. STRATEGIES

Investment styles:
- `buy_and_hold`
- `fix_and_flip`
- `owner_occupant`

Each property and market carries:
- `strategy_tags` and
- per-strategy scores.

## 3. DATA SCHEMA

(… include property-level and market-level schemas as defined …)

## 4. DEAL SCORING

(… include 3 scoring formulas and how they’re combined …)

## 5. CRAWLING RULES

- TLDs: .com, .org, .net, .info, and country-specific TLDs.
- Respect robots.txt, TOS.
- Rate limits per domain and per country.

## 6. OUTPUT & INTEGRATION

- US-specific outputs
- Global-specific outputs
- Integration into:
  - STRATEGY/MARKET_SHIFT_STRATEGY.md
  - STRATEGY/LISTING_STRATEGY.yaml
  - ANALYTICS/BEST_DEALS_* files

  Example Code-Oriented Config (YAML)
Again, because these documents can only be used in code execution, here’s a concrete YAML that a dev could wire up:

regions:
  tier1_us:
    countries: ["US"]
    scrape_frequency:
      properties: "hourly"
      markets: "daily"
  tier2_global:
    countries: ["CA", "GB", "DE", "NL", "FR", "ES", "AU", "NZ", "MX", "BR", "AE", "SG"]
    scrape_frequency:
      properties: "daily"
      markets: "weekly"

strategies:
  - id: "buy_and_hold"
    name: "Buy & Hold Rentals"
  - id: "fix_and_flip"
    name: "Fix & Flip"
  - id: "owner_occupant"
    name: "Owner-Occupant"

deal_scoring:
  property:
    buy_and_hold:
      weights:
        yield: 0.45
        stability: 0.25
        tenant_demand: 0.20
        landlord_friendliness: 0.10
    fix_and_flip:
      weights:
        discount: 0.50
        renovation_potential: 0.25
        velocity: 0.20
        risk_penalty: -0.15
    owner_occupant:
      weights:
        affordability: 0.35
        stability: 0.25
        qol: 0.25
        liquidity: 0.15

tlds:
  allowed:
    - ".com"
    - ".org"
    - ".net"
    - ".info"
  respect_robots: true
  max_rps_per_domain: 1

output:
  us:
    properties_raw: "DATA/PROPERTIES/us_properties_raw_{{date}}.csv"
    properties_scored: "DATA/PROPERTIES/us_properties_scored_{{date}}.csv"
    markets_scored: "DATA/MARKETS/us_markets_scored_{{date}}.csv"
    best_deals: "ANALYTICS/US_BEST_DEALS_REPORT.json"
    best_markets: "ANALYTICS/US_BEST_MARKETS_REPORT.json"
  global:
    properties_raw: "DATA/PROPERTIES/global_properties_raw_{{date}}.csv"
    properties_scored: "DATA/PROPERTIES/global_properties_scored_{{date}}.csv"
    markets_scored: "DATA/MARKETS/global_markets_scored_{{date}}.csv"
    best_deals: "ANALYTICS/GLOBAL_BEST_DEALS_REPORT.json"
    best_markets: "ANALYTICS/GLOBAL_BEST_MARKETS_REPORT.json"

    +====================================================================================+
|              REALTOR-AGENT LANDOS – SCRAPE INTEGRATION (US + GLOBAL)              |
|                    FOLDERS, FILES, FLOWS, DASHBOARDS (ASCII)                      |
+====================================================================================+

PART 1 – LANDOS FOLDER TREE WITH SCRAPE OUTPUTS
====================================================================================

📁 REALTOR_AGENT_SYSTEM/
│
├── 📁 ADMIN/
├── 📁 CORE/
├── 📁 STRATEGY/
│   ├── ANNUAL_STRATEGY.md
│   ├── LEAD_STRATEGY.yaml
│   ├── LISTING_STRATEGY.yaml
│   ├── LEVERAGE_STRATEGY.yaml
│   ├── MARKETING_STRATEGY.yaml
│   ├── MARKET_SHIFT_STRATEGY.md        ◀─ UPDATED using US+Global market scores
│   ├── TIME_STRATEGY.yaml
│   ├── FINANCIAL_STRATEGY.yaml
│   └── STRATEGY_SIMULATIONS/
│       ├── sim_us_markets_YYYYMM.json
│       ├── sim_global_markets_YYYYMM.json
│       └── ...
│
├── 📁 OPERATIONS/
│   ├── DAILY_PLAN.md
│   ├── LEAD_GEN_BLOCK.md
│   ├── ACTIVE_TASKS.jsonl
│   ├── CALENDAR_SYNC.ics
│   ├── PIPELINE_SNAPSHOT.json
│   ├── RED_GREEN_DASHBOARD.json
│   └── NEXT_BEST_ACTION.md
│
├── 📁 DATA/
│   ├── 📁 CONTACTS/
│   ├── 📁 LISTINGS/
│   ├── 📁 TRANSACTIONS/
│   ├── 📁 FINANCIALS/
│   ├── 📁 GOALS_ACTUALS/
│   ├── 📁 BACKUPS/
│   │
│   ├── 📁 PROPERTIES/                 ◀─ NEW SCRAPED PROPERTY DATA
│   │   ├── us_properties_raw_YYYYMMDD.csv
│   │   ├── us_properties_scored_YYYYMMDD.csv
│   │   ├── global_properties_raw_YYYYMMDD.csv
│   │   └── global_properties_scored_YYYYMMDD.csv
│   │
│   └── 📁 MARKETS/                    ◀─ NEW SCRAPED MARKET DATA
│       ├── us_markets_scored_YYYYMMDD.csv
│       └── global_markets_scored_YYYYMMDD.csv
│
├── 📁 ANALYTICS/
│   ├── WEEKLY_REPORT.md
│   ├── MONTHLY_REPORT.md
│   ├── LEAD_FUNNEL_REPORT.json
│   ├── SOURCE_ROI_REPORT.json
│   ├── CONVERSION_REPORT.json
│   ├── FINANCIAL_DASHBOARD.json
│   ├── TEAM_PERFORMANCE.json
│   ├── MARKET_SNAPSHOT.json
│   │
│   ├── US_BEST_DEALS_REPORT.json        ◀─ top US properties (by strategy)
│   ├── GLOBAL_BEST_DEALS_REPORT.json    ◀─ top global properties (by strategy)
│   ├── US_BEST_MARKETS_REPORT.json      ◀─ top US markets by strategy
│   └── GLOBAL_BEST_MARKETS_REPORT.json  ◀─ top global markets by strategy
│
├── 📁 WORKFLOWS/
│   ├── WORKFLOW_REGISTRY.yaml
│   ├── lead_nurture_sequence.yaml
│   ├── listing_lifecycle.yaml
│   ├── transaction_flow.yaml
│   ├── campaign_automation.yaml
│   ├── coaching_prompts.yaml
│   └── EXECUTION_LOG.jsonl
│
├── 📁 SCRIPTS_DIALOGUES/
├── 📁 MARKETING/
├── 📁 CLIENTS/
├── 📁 TEAM/
├── 📁 LEARNING/
├── 📁 SYSTEMS_TOOLS/
├── 📁 LOGS/
└── 📁 ARCHIVE/


PART 2 – DATA FLOW: SCRAPER → DATA/ → ANALYTICS/ → STRATEGY/ → UI
====================================================================================

HIGH-LEVEL FLOW
----------------

INTERNET (US & Global real estate sites)
      |
      v
+---------------------------+
|  SCRAPE ENGINE (US/GLOB) |
+---------------------------+
      |
      v
+---------------------------+
|   RAW DATA (DATA/...)    |
+---------------------------+
      |
      v
+---------------------------+
|  SCORING & AGGREGATION   |
+---------------------------+
      |
      v
+---------------------------+
|  ANALYTICS REPORTS       |
+---------------------------+
      |
      v
+---------------------------+
|  STRATEGY LAYER          |
+---------------------------+
      |
      v
+---------------------------+
|  UI DASHBOARDS & TASKS   |
+---------------------------+


DETAIL: US vs GLOBAL PIPELINE
-----------------------------

```txt
                     +------------------------------+
INTERNET (US sites)  | SCRAPER_US                   |
-------------------> | - respect robots/TOS         |
                     | - property & market schemas  |
                     +--------------+---------------+
                                    |
                                    v
                     +------------------------------+
                     | DATA/PROPERTIES/             |
                     |  - us_properties_raw_*.csv   |
                     |  - us_properties_scored_*.csv|
                     +--------------+---------------+
                                    |
                                    v
                     +------------------------------+
                     | DATA/MARKETS/                |
                     |  - us_markets_scored_*.csv   |
                     +--------------+---------------+
                                    |
                                    v
                     +------------------------------+
                     | ANALYTICS/                   |
                     |  - US_BEST_DEALS_REPORT.json |
                     |  - US_BEST_MARKETS_REPORT.json
                     +--------------+---------------+
                                    |
                                    v
                     +------------------------------+
                     | STRATEGY LAYER (L0.5)        |
                     |  - MARKET_SHIFT_STRATEGY.md  |
                     |  - LISTING_STRATEGY.yaml     |
                     |  - LEAD_STRATEGY.yaml        |
                     +--------------+---------------+
                                    |
                                    v
                     +------------------------------+
                     | UI DASHBOARDS (L5)           |
                     |  - US Markets / Deals views  |
                     |  - Actions & workflows       |
                     +------------------------------+


                     +------------------------------+
INTERNET (Global)    | SCRAPER_GLOBAL               |
-------------------> | - multi-currency            |
                     | - ccTLDs, global schemas    |
                     +--------------+--------------+
                                    |
                                    v
                     +------------------------------+
                     | DATA/PROPERTIES/             |
                     |  - global_properties_raw_*.csv
                     |  - global_properties_scored_*.csv
                     +--------------+--------------+
                                    |
                                    v
                     +------------------------------+
                     | DATA/MARKETS/                |
                     |  - global_markets_scored_*.csv
                     +--------------+--------------+
                                    |
                                    v
                     +------------------------------+
                     | ANALYTICS/                   |
                     |  - GLOBAL_BEST_DEALS_REPORT.json
                     |  - GLOBAL_BEST_MARKETS_REPORT.json
                     +--------------+--------------+
                                    |
                                    v
                     +------------------------------+
                     | STRATEGY LAYER (L0.5)        |
                     |  - MARKET_SHIFT_STRATEGY.md  |
                     |  - ANNUAL_STRATEGY.md        |
                     |  - EXPANSION sections        |
                     +--------------+--------------+
                                    |
                                    v
                     +------------------------------+
                     | UI DASHBOARDS (L5)           |
                     |  - Global Markets / Deals    |
                     |  - Expansion recommendations |
                     +------------------------------+

 HOW SCRAPE DATA FEEDS STRATEGY LAYER (L0.5)
STRATEGY LAYER MODULES (RECAP)
S-LEADS (Lead-Generation Strategy)
S-LISTINGS (Listings-First Strategy)
S-LEVERAGE (People / Systems / Tools)
S-MARKETING (Marketing Strategy)
S-MARKET (Market-Shift Strategy)
S-TIME_80_20 (Time / 80–20 Strategy)
S-SERVICE (Service/Fiduciary Strategy)
S-FINANCE (Economic / Budget / Net Strategy)      

+-------------------------------------------+
|  STRATEGY LAYER (L0.5)                    |
+-------------------------------------------+
| INPUT FILES:                              |
|  - DATA/MARKETS/us_markets_scored_*.csv   |
|  - DATA/MARKETS/global_markets_scored_*.csv
|  - ANALYTICS/US_BEST_DEALS_REPORT.json    |
|  - ANALYTICS/GLOBAL_BEST_DEALS_REPORT.json
|  - ANALYTICS/US_BEST_MARKETS_REPORT.json  |
|  - ANALYTICS/GLOBAL_BEST_MARKETS_REPORT.json
+-------------------------------------------+
        |             |             |
        v             v             v
   +----------+  +-----------+  +-----------+
   | S-MARKET |  | S-LISTINGS|  | S-LEADS   |
   +----------+  +-----------+  +-----------+
        |             |             |
        v             v             v
 MARKET_SHIFT_   LISTING_       LEAD_
 STRATEGY.md     STRATEGY.yaml  STRATEGY.yaml
 (US + Global)   (US bias)      (US/Global for
                                outbound prospecting)

                                HOW EACH STRATEGY MODULE USES SCRAPE DATA

                                S-MARKET (Market-Shift Strategy)
Reads:
us_markets_scored_*.csv
global_markets_scored_*.csv
US_BEST_MARKETS_REPORT.json
GLOBAL_BEST_MARKETS_REPORT.json
Writes:
STRATEGY/MARKET_SHIFT_STRATEGY.md
sections:
“US Opportunity Markets” (top US cities/zips by score_buy_and_hold, score_fix_and_flip, score_owner_occupant)
“Global Opportunity Markets” (same, globally)
“Markets to Deprioritize or Exit”
S-LISTINGS (Listings Strategy)
Reads:
US_BEST_DEALS_REPORT.json (especially fix & flip / owner-occupant tags)
Writes:
STRATEGY/LISTING_STRATEGY.yaml
Focus listing efforts in markets with high score_owner_occupant or good flip liquidity.
Prioritized target cities/zip codes for listing-based prospecting.
S-LEADS (Lead-Generation Strategy)
Reads:
US_BEST_MARKETS_REPORT.json
GLOBAL_BEST_MARKETS_REPORT.json (for expansion)
Writes:
STRATEGY/LEAD_STRATEGY.yaml
Adjusts source mix by market opportunity:
More geo-farm & FSBO/expired in top US opportunity markets.
Separate section for international referral or relocation leads from high-score global markets.
S-FINANCE / S-TIME_80_20 / S-LEVERAGE
Use where the money & opportunity is:
Reallocate marketing spend to best-scoring US/Global markets.
Allocate time blocks for prospecting in those markets.
Justify new hires focused on expansion regions.
PART 4 – UI DASHBOARDS: US VS GLOBAL VIEWS
TOP-LEVEL UI INTEGRATION

+----------------------------------------------------------+
| L5: UI DASHBOARDS                                        |
+----------------------------------------------------------+
| [HOME]                                                   |
| [US MARKETS]  [GLOBAL MARKETS]                           |
| [BEST DEALS]  [STRATEGY]  [TASKS]                        |
+----------------------------------------------------------+

US Markets Dashboard
Reads:

ANALYTICS/US_BEST_MARKETS_REPORT.json
DATA/MARKETS/us_markets_scored_*.csv
Shows:

Top N US cities/zips ranked by:
score_buy_and_hold
score_fix_and_flip
score_owner_occupant
Trend charts per top market (price, rent, DOM).
Buttons:
[Focus Listing Strategy Here]
-> updates LISTING_STRATEGY.yaml (via strategy module).
[Create Geo-Farm Plan]
-> new entry in MARKETING/CAMPAIGNS/ plus WORKFLOWS/ sequence.
[Add to Lead Strategy]
-> update LEAD_STRATEGY.yaml target markets.
Global Markets Dashboard
Reads:

ANALYTICS/GLOBAL_BEST_MARKETS_REPORT.json
DATA/MARKETS/global_markets_scored_*.csv
Shows:

Top N global cities/countries by strategy score.
FX-normalized yields & price levels.
Buttons:
[Mark as Expansion Market]
-> writes to ANNUAL_STRATEGY.md & MARKET_SHIFT_STRATEGY.md.
[Create Expansion Simulation]
-> new file in STRATEGY/STRATEGY_SIMULATIONS/sim_global_markets_*.json.
Best Deals Dashboard (US + Global)
Reads:

US_BEST_DEALS_REPORT.json
GLOBAL_BEST_DEALS_REPORT.json
Shows:

Tabs:
US – Buy & Hold
US – Fix & Flip
US – Owner-Occupant
Global – Buy & Hold
Global – Fix & Flip
Global – Owner-Occupant
For each tab: ranked property list.
Buttons for each property:

[Save as Lead]
Creates a contact / prospect in CLIENTS/ and DB.
[Create Outreach Plan]
Spawns tasks & campaigns in OPERATIONS/ and WORKFLOWS/.
[Add to Strategy Notes]
Appends to MARKET_SHIFT_STRATEGY.md under “Example Deals” section.
Strategy Console (US + Global)
Reads:

MARKET_SHIFT_STRATEGY.md
ANNUAL_STRATEGY.md
LEAD_STRATEGY.yaml
LISTING_STRATEGY.yaml
Shows:

Highlighted US targets.
Highlighted global targets.
Buttons:
[Sync Strategy with Latest Scrapes]
Runs S-MARKET, S-LEADS, S-LISTINGS using fresh ANALYTICS/*.
[Simulate Next 12 Months]
Writes to STRATEGY/STRATEGY_SIMULATIONS/ and shows results.
PART 5 – COMBINED STACK WITH SCRAPE FEEDS (ASCII)

+================================================================================+
|                     FULL REALTOR-AGENT LANDOS STACK                           |
+================================================================================+

INTERNET (US & Global real estate sites)
   |
   v
+------------------------------+
| SCRAPER_US / SCRAPER_GLOBAL |
+------------------------------+
   |
   v
+------------------------------+
|   DATA LAYER (DATA/)        |
| - PROPERTIES (US/GLOBAL)    |
| - MARKETS (US/GLOBAL)       |
+------------------------------+
   |
   v
+------------------------------+
| ANALYTICS LAYER (ANALYTICS/)|
| - US_BEST_DEALS_REPORT      |
| - GLOBAL_BEST_DEALS_REPORT  |
| - US_BEST_MARKETS_REPORT    |
| - GLOBAL_BEST_MARKETS_REPORT|
+------------------------------+
   |
   v
+------------------------------+
| STRATEGY LAYER (L0.5)       |
| - MARKET_SHIFT_STRATEGY.md  |
| - LISTING_STRATEGY.yaml     |
| - LEAD_STRATEGY.yaml        |
| - ANNUAL_STRATEGY.md        |
+------------------------------+
   |
   v
+------------------------------+
| WORKFLOWS (L2)              |
| - lead_nurture_sequence     |
| - listing_lifecycle         |
| - campaign_automation       |
+------------------------------+
   |
   v
+------------------------------+
| DOMAIN MODULES (L1)         |
| - LeadGen, Listings, Buyers |
| - Transactions, Marketing   |
+------------------------------+
   |
   v
+------------------------------+
| UI DASHBOARDS (L5)          |
| - US Markets / Global Mkts  |
| - Best Deals (US/Global)    |
| - Strategy Console          |
+------------------------------+
   |
   v
+------------------------------+
| AGENT ACTIONS               |
| - Prospect, List, Invest    |
| - Expand to new markets     |
+------------------------------+

Exact file paths for all US + global scrape outputs in DATA/, ANALYTICS/, and how they touch STRATEGY/.
A clear flow from raw internet data → scored deals/markets → strategy decisions → dashboards and tasks.