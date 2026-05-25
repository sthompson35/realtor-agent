"""
Negotiator Bot — Bot 7: Counter-offer analysis and deal stage advancement.
"""

from __future__ import annotations
import logging
from datetime import datetime
from typing import Any

from realtor_agent.bots.base import BaseBot, BotResult
from realtor_agent.core.models import DealIntakeModel, SessionLocal

logger = logging.getLogger(__name__)

# Stage progression map
_ADVANCE_MAP: dict[str, str] = {
    "lead":           "qualified",
    "qualified":      "offer_sent",
    "offer_sent":     "under_contract",
    "under_contract": "under_contract",  # stays until closed
}

# ROI threshold to advance aggressively
_HIGH_ROI_THRESHOLD = 0.20


def _recommend_strategy(deal: dict) -> dict[str, Any]:
    """Derive a negotiation recommendation from underwriting data."""
    mao    = float(deal.get("best_mao") or 0)
    price  = float(deal.get("contract_price") or 0)
    roi    = float(deal.get("best_roi") or 0)
    strats = deal.get("viable_strategies", [])

    if mao <= 0 or price <= 0:
        return {"action": "pass", "reason": "No viable MAO calculated"}

    spread_pct = (mao - price) / price if price else 0

    if spread_pct >= 0.10 and roi >= _HIGH_ROI_THRESHOLD:
        action   = "offer_at_mao"
        offer    = mao
        reason   = f"Strong spread ({spread_pct:.1%}) and ROI ({roi:.1%}) — offer at MAO"
    elif spread_pct >= 0:
        action   = "offer_below_mao"
        offer    = round(mao * 0.95, -3)
        reason   = f"Moderate spread — open at 95% of MAO to leave room"
    else:
        action   = "negotiate_creative"
        offer    = price
        reason   = f"Price exceeds MAO — explore {', '.join(strats[:2]) or 'creative finance'}"

    return {
        "action":         action,
        "recommended_offer": offer,
        "mao":            mao,
        "spread_pct":     round(spread_pct, 4),
        "reason":         reason,
        "preferred_strategy": strats[0] if strats else None,
    }


class NegotiatorBot(BaseBot):
    """
    Bot 7 — Negotiator.

    Reads approved deals from the underwriter, builds a negotiation
    recommendation for each, and advances the deal's status
    to the next stage.

    Context in:  context["underwriter"]["approved"]
    Context out: context["negotiator"]["negotiations"]
    """

    name = "negotiator"

    def __init__(self, config=None, database=None, **kwargs):
        self.config = config

    def run(self, context: dict) -> BotResult:
        approved: list[dict] = context.get("underwriter", {}).get("approved", [])

        if not approved:
            logger.info("Negotiator: no approved deals to negotiate")
            return BotResult({"negotiations": [], "advanced": 0})

        db = SessionLocal()
        negotiations: list[dict[str, Any]] = []
        advanced = 0

        try:
            for deal in approved:
                deal_id = deal.get("deal_id", "")
                rec     = _recommend_strategy(deal)

                row = db.query(DealIntakeModel).filter_by(deal_id=deal_id).first()
                if row:
                    current_stage  = row.status or "lead"
                    next_stage     = _ADVANCE_MAP.get(current_stage, current_stage)
                    if next_stage != current_stage:
                        row.status = next_stage
                        advanced += 1

                negotiations.append({
                    "deal_id":   deal_id,
                    "address":   deal.get("address"),
                    "recommendation": rec,
                    "stage_advanced": advanced > 0,
                })

            db.commit()
        except Exception as exc:
            db.rollback()
            logger.error("Negotiator DB error: %s", exc)
        finally:
            db.close()

        logger.info("Negotiator: %d deals advanced, %d negotiations recorded",
                    advanced, len(negotiations))
        return BotResult({
            "negotiations": negotiations,
            "advanced":     advanced,
            "total":        len(negotiations),
        })
