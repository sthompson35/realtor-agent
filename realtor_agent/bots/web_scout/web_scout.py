"""
Web Scout Bot — Bot 1: Listings Intake.
Generates and persists synthetic deal leads for the pipeline.
"""

from __future__ import annotations
import hashlib
import logging
import random
from datetime import datetime
from typing import Any

from realtor_agent.bots.base import BaseBot, BotResult
from realtor_agent.core.models import DealIntakeModel, SessionLocal

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Synthetic listing templates — realistic REI deal scenarios
# ---------------------------------------------------------------------------

_MARKETS = [
    ("Austin",       "TX", "Travis",    "787"),
    ("Dallas",       "TX", "Dallas",    "752"),
    ("Houston",      "TX", "Harris",    "770"),
    ("San Antonio",  "TX", "Bexar",     "782"),
    ("Denver",       "CO", "Denver",    "802"),
    ("Phoenix",      "AZ", "Maricopa",  "850"),
    ("Raleigh",      "NC", "Wake",      "276"),
    ("Nashville",    "TN", "Davidson",  "372"),
    ("Orlando",      "FL", "Orange",    "328"),
    ("Tampa",        "FL", "Hillsborough","336"),
]

_STREET_NAMES = [
    "Oak Creek Dr", "Maple Ave", "Pine Ridge Rd", "Cedar Ln", "Elm St",
    "Birch Ct", "Willow Way", "Sunset Blvd", "River Rd", "Valley View Dr",
    "Hillcrest Ave", "Lakewood Dr", "Meadow Ln", "Forest Glen Rd", "Summit Dr",
]

_ASSET_TYPES = [
    ("SFR",    0.65),
    ("Duplex", 0.15),
    ("Land",   0.12),
    ("4plex",  0.05),
    ("MF",     0.03),
]


def _weighted_choice(choices):
    population, weights = zip(*choices)
    return random.choices(population, weights=weights, k=1)[0]


def _make_listing(seed: int) -> dict[str, Any]:
    rng = random.Random(seed)
    city, state, county, zip_prefix = rng.choice(_MARKETS)
    street = f"{rng.randint(100, 9999)} {rng.choice(_STREET_NAMES)}"
    zip_code = f"{zip_prefix}{rng.randint(10, 99)}"
    address = f"{street}, {city}, {state}"

    asset_type = _weighted_choice(_ASSET_TYPES)

    if asset_type == "Land":
        arv       = round(rng.uniform(40_000, 180_000), -3)
        price     = round(arv * rng.uniform(0.45, 0.75), -3)
        rehab     = 0.0
        sqft      = 0
        rent      = 0.0
        acres     = round(rng.uniform(0.5, 10.0), 2)
        zoning    = rng.choice(["R1", "R2", "AG", "RR"])
        buildable = rng.random() > 0.15
        flood     = rng.choices(["X", "AE", "VE"], weights=[0.80, 0.15, 0.05])[0]
    elif asset_type in ("Duplex", "4plex", "MF"):
        units     = {"Duplex": 2, "4plex": 4, "MF": 8}[asset_type]
        sqft      = rng.randint(800, 1_400) * units
        arv       = round(sqft * rng.uniform(100, 180), -3)
        price     = round(arv * rng.uniform(0.60, 0.80), -3)
        rehab     = round(arv * rng.uniform(0.05, 0.20), -3)
        rent      = round(rng.uniform(900, 1_600) * units, -2)
        acres     = 0.0
        zoning    = "R2"
        buildable = False
        flood     = "X"
    else:  # SFR
        sqft      = rng.randint(1_000, 3_000)
        arv       = round(sqft * rng.uniform(110, 200), -3)
        price     = round(arv * rng.uniform(0.55, 0.80), -3)
        rehab     = round(arv * rng.uniform(0.05, 0.22), -3)
        rent      = round(rng.uniform(1_200, 2_800), -2)
        acres     = 0.0
        zoning    = "R1"
        buildable = False
        flood     = rng.choices(["X", "AE"], weights=[0.90, 0.10])[0]

    taxes    = round(arv * rng.uniform(0.010, 0.025), -1)
    insur    = round(arv * rng.uniform(0.004, 0.010), -1)
    hoa      = round(rng.choice([0, 0, 0, 150, 250, 400]), -1)
    dom      = rng.randint(1, 180)

    deal_id = "WS-" + hashlib.md5(address.encode()).hexdigest()[:8].upper()

    return {
        "deal_id":       deal_id,
        "address":       address,
        "city":          city,
        "state":         state,
        "county":        county,
        "zip_code":      zip_code,
        "asset_type":    asset_type,
        "contract_price": price,
        "asking_price":  price,
        "arv":           arv,
        "rehab_cost":    rehab,
        "sqft":          sqft,
        "monthly_rent":  rent,
        "taxes":         taxes,
        "insurance":     insur,
        "hoa":           hoa,
        "dom":           dom,
        "acres":         acres,
        "zoning":        zoning,
        "buildable":     buildable,
        "flood_zone":    flood,
        "source":        "web_scout",
        "scraped_at":    datetime.utcnow().isoformat(),
    }


# ---------------------------------------------------------------------------
# Bot
# ---------------------------------------------------------------------------

class WebScoutBot(BaseBot):
    """
    Bot 1 — Web Scout.

    Generates synthetic deal listings and persists them as DealIntakeModel rows.
    In production, replace _make_listing() with real API / scrape calls.

    Context in:  (none required)
    Context out: context["web_scout"]["listings"]  — list of raw listing dicts
    """

    name = "web_scout"

    def __init__(self, config=None, database=None, num_leads: int = 10, **kwargs):
        self.config = config
        self.num_leads = num_leads

    def run(self, context: dict) -> BotResult:
        num = context.get("num_leads", self.num_leads)
        logger.info("WebScout: generating %d listings", num)

        seed_base = int(datetime.utcnow().timestamp()) // 3600  # changes each hour
        raw_listings = [_make_listing(seed_base + i) for i in range(num)]

        db = SessionLocal()
        new_count = 0
        try:
            for raw in raw_listings:
                exists = db.query(DealIntakeModel).filter_by(deal_id=raw["deal_id"]).first()
                if exists:
                    continue
                row = DealIntakeModel(
                    deal_id       = raw["deal_id"],
                    address       = raw["address"],
                    city          = raw["city"],
                    state         = raw["state"],
                    county        = raw["county"],
                    zip_code      = raw["zip_code"],
                    asset_type    = raw["asset_type"],
                    contract_price= raw["contract_price"],
                    arv           = raw["arv"],
                    rehab_cost    = raw["rehab_cost"],
                    monthly_rent  = raw["monthly_rent"],
                    taxes         = raw["taxes"],
                    insurance     = raw["insurance"],
                    hoa           = raw["hoa"],
                    dom           = raw["dom"],
                    acres         = raw["acres"],
                    zoning        = raw["zoning"],
                    buildable     = raw["buildable"],
                    flood_zone    = raw["flood_zone"],
                    status        = "lead",
                    source        = "web_scout",
                )
                db.add(row)
                new_count += 1
            db.commit()
        except Exception as exc:
            db.rollback()
            logger.error("WebScout DB error: %s", exc)
        finally:
            db.close()

        logger.info("WebScout: %d new listings saved (%d total generated)", new_count, num)
        return BotResult({
            "listings":  raw_listings,
            "total":     num,
            "new":       new_count,
        })
