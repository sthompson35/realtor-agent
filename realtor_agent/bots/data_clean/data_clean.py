"""
Data Clean Bot — Bot 2: Data Clean & Enrichment.
Normalizes listings from web_scout, fills missing fields, deduplicates.
"""

from __future__ import annotations
import logging
import re
from typing import Any

from realtor_agent.bots.base import BaseBot, BotResult

logger = logging.getLogger(__name__)

_STATE_ABBREVS = {s.lower(): s.upper() for s in [
    "AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA","HI","ID","IL","IN","IA",
    "KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ",
    "NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT",
    "VA","WA","WV","WI","WY","DC",
]}


def _normalize_state(raw: str) -> str:
    if not raw:
        return ""
    upper = raw.strip().upper()
    if len(upper) == 2 and upper in _STATE_ABBREVS.values():
        return upper
    return _STATE_ABBREVS.get(raw.strip().lower(), raw.strip()[:2].upper())


def _normalize_zip(raw: Any) -> str:
    s = str(raw or "").strip()
    digits = re.sub(r"\D", "", s)[:5]
    return digits.zfill(5) if digits else ""


def _fill_missing(listing: dict) -> dict:
    """Impute obviously missing or zero fields."""
    out = dict(listing)

    sqft = float(out.get("sqft") or 0)
    if sqft <= 0 and out.get("asset_type", "SFR") not in ("Land",):
        sqft = 1_400.0
        out["sqft"] = sqft

    price = float(out.get("contract_price") or out.get("asking_price") or out.get("price") or 0)

    arv = float(out.get("arv") or 0)
    if arv <= 0 and price > 0:
        arv = round(price * 1.35, -3)
        out["arv"] = arv

    if float(out.get("rehab_cost") or 0) <= 0 and arv > 0:
        ratio = 0.0 if out.get("asset_type") == "Land" else 0.10
        out["rehab_cost"] = round(arv * ratio, -2)

    if float(out.get("taxes") or 0) <= 0 and arv > 0:
        out["taxes"] = round(arv * 0.015, -1)

    if float(out.get("insurance") or 0) <= 0 and arv > 0:
        out["insurance"] = round(arv * 0.006, -1)

    out["state"]    = _normalize_state(out.get("state", ""))
    out["zip_code"] = _normalize_zip(out.get("zip_code") or out.get("zip", ""))
    out["asset_type"] = out.get("asset_type") or "SFR"
    out["flood_zone"] = out.get("flood_zone") or "X"

    return out


class DataCleanBot(BaseBot):
    """
    Bot 2 — Data Clean & Enrichment.

    Reads raw listings from context["web_scout"]["listings"],
    normalises fields, deduplicates by address, and returns a cleaned list.

    Context in:  context["web_scout"]["listings"]
    Context out: context["data_clean"]["listings"]
    """

    name = "data_clean"

    def __init__(self, config=None, database=None, **kwargs):
        self.config = config

    def run(self, context: dict) -> BotResult:
        raw: list[dict] = context.get("web_scout", {}).get("listings", [])

        if not raw:
            logger.info("DataClean: no listings to clean")
            return BotResult({"listings": [], "cleaned": 0, "dupes_removed": 0})

        seen: set[str] = set()
        cleaned: list[dict] = []
        dupes = 0

        for listing in raw:
            key = (listing.get("address") or "").lower().strip()
            if key and key in seen:
                dupes += 1
                continue
            if key:
                seen.add(key)
            cleaned.append(_fill_missing(listing))

        logger.info("DataClean: %d cleaned, %d dupes removed", len(cleaned), dupes)
        return BotResult({
            "listings":     cleaned,
            "cleaned":      len(cleaned),
            "dupes_removed": dupes,
        })
