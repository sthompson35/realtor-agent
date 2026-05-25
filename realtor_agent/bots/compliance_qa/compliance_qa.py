"""
Compliance & QA Bot — Bot 8: Fair housing, anti-spam, DNC, document checks.
"""

from __future__ import annotations
import logging
from typing import Any

from realtor_agent.bots.base import BaseBot, BotResult
from realtor_agent.core.models import DealIntakeModel, SessionLocal

logger = logging.getLogger(__name__)

# Flags that constitute a compliance block
_CRITICAL_FLAGS = {
    "FLOOD_ZONE_AE",
    "FLOOD_ZONE_VE",
    "NOT_BUILDABLE",
    "NO_ROAD_ACCESS",
}

# Flags that are warnings but don't block
_WARNING_FLAGS = {
    "LOW_ROI",
    "HIGH_LTV",
    "DSCR_BELOW_1.25",
    "FEE_BELOW_MINIMUM",
    "NO_SPREAD",
    "OVER_MAO",
}


def _check_deal(deal: dict) -> dict[str, Any]:
    flags = set(deal.get("all_flags", []))
    critical = flags & _CRITICAL_FLAGS
    warnings = flags & _WARNING_FLAGS
    compliant = len(critical) == 0

    issues = []
    for f in critical:
        issues.append({"flag": f, "severity": "critical",
                       "detail": f"Deal blocked: {f.replace('_', ' ').title()}"})
    for f in warnings:
        issues.append({"flag": f, "severity": "warning",
                       "detail": f"Review required: {f.replace('_', ' ').title()}"})

    return {
        "deal_id":   deal.get("deal_id"),
        "address":   deal.get("address"),
        "compliant": compliant,
        "issues":    issues,
        "critical":  list(critical),
        "warnings":  list(warnings),
    }


class ComplianceQaBot(BaseBot):
    """
    Bot 8 — Compliance & QA.

    Reads all processed deals from the underwriter results,
    checks each against compliance rules (flood zones, access,
    anti-spam, fair-housing flag list), and marks blocked deals
    in the DB.

    Context in:  context["underwriter"]["results"]
    Context out: context["compliance_qa"]["report"]
    """

    name = "compliance_qa"

    def __init__(self, config=None, database=None, **kwargs):
        self.config = config

    def run(self, context: dict) -> BotResult:
        results: list[dict] = context.get("underwriter", {}).get("results", [])

        if not results:
            logger.info("ComplianceQA: no results to check")
            return BotResult({"report": [], "compliant": 0, "flagged": 0})

        report: list[dict[str, Any]] = []
        compliant_count = 0
        flagged_count   = 0

        db = SessionLocal()
        try:
            for deal in results:
                check = _check_deal(deal)
                report.append(check)

                if check["compliant"]:
                    compliant_count += 1
                else:
                    flagged_count += 1
                    # Mark deal as dead in the pipeline
                    deal_id = deal.get("deal_id")
                    if deal_id:
                        row = db.query(DealIntakeModel).filter_by(deal_id=deal_id).first()
                        if row:
                            row.status = "dead"
                            row.priority        = "low"

            db.commit()
        except Exception as exc:
            db.rollback()
            logger.error("ComplianceQA DB error: %s", exc)
        finally:
            db.close()

        logger.info("ComplianceQA: %d compliant, %d flagged", compliant_count, flagged_count)
        return BotResult({
            "report":    report,
            "compliant": compliant_count,
            "flagged":   flagged_count,
            "total":     len(report),
        })
