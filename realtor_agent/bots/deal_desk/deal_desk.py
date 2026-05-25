"""
Deal Desk Bot — Bot 4: Deal Desk.
Generates offer summaries and term sheets for underwriter-approved deals.
"""

from __future__ import annotations
import logging
from datetime import datetime, timedelta
from typing import Any

from realtor_agent.bots.base import BaseBot, BotResult
from realtor_agent.core.models import DealIntakeModel, SessionLocal

logger = logging.getLogger(__name__)


def _format_currency(v: float) -> str:
    return f"${v:,.0f}"


def _offer_summary(deal: dict) -> str:
    """Generate a plain-text offer summary for a deal."""
    strats = deal.get("viable_strategies", [])
    mao    = deal.get("best_mao", 0) or 0
    arv    = deal.get("arv", 0) or 0
    price  = deal.get("contract_price", 0) or 0
    rehab  = deal.get("rehab_cost", 0) or 0

    strategy_line = ", ".join(strats) if strats else "None identified"
    close_date    = (datetime.utcnow() + timedelta(days=30)).strftime("%B %d, %Y")

    lines = [
        f"OFFER SUMMARY — {deal.get('address', 'Unknown')}",
        f"Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}",
        "",
        f"  Asking Price : {_format_currency(price)}",
        f"  ARV          : {_format_currency(arv)}",
        f"  Rehab Est.   : {_format_currency(rehab)}",
        f"  MAO          : {_format_currency(mao)}",
        "",
        f"  Viable Strategies : {strategy_line}",
        f"  Proposed Close    : {close_date}",
        f"  Earnest Money     : {_format_currency(min(1_000, price * 0.01))}",
        "",
        "  Terms: Cash / Hard Money / Creative Finance per strategy above.",
        "  Inspection period: 10 business days.",
        "  Title company: Seller's choice or mutually agreed.",
    ]
    return "\n".join(lines)


class DealDeskBot(BaseBot):
    """
    Bot 4 — Deal Desk.

    For each approved deal from the underwriter, generates an offer summary
    and persists it as a note on the DealIntakeModel record.

    Context in:  context["underwriter"]["approved"]
    Context out: context["deal_desk"]["offers"]
    """

    name = "deal_desk"

    def __init__(self, config=None, database=None, **kwargs):
        self.config = config

    def run(self, context: dict) -> BotResult:
        approved: list[dict] = context.get("underwriter", {}).get("approved", [])

        if not approved:
            logger.info("DealDesk: no approved deals to process")
            return BotResult({"offers": [], "total": 0})

        db = SessionLocal()
        offers: list[dict[str, Any]] = []

        try:
            for deal in approved:
                summary = _offer_summary(deal)
                deal_id = deal.get("deal_id")

                # Persist summary as notes on the DB record
                if deal_id:
                    row = db.query(DealIntakeModel).filter_by(deal_id=deal_id).first()
                    if row:
                        row.notes = summary
                        row.pipeline_status = "qualified"

                offers.append({
                    "deal_id":  deal_id,
                    "address":  deal.get("address"),
                    "mao":      deal.get("best_mao"),
                    "strategies": deal.get("viable_strategies", []),
                    "summary":  summary,
                })

            db.commit()
        except Exception as exc:
            db.rollback()
            logger.error("DealDesk DB error: %s", exc)
        finally:
            db.close()

        logger.info("DealDesk: %d offer summaries generated", len(offers))
        return BotResult({"offers": offers, "total": len(offers)})
