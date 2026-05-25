"""
Underwriter Bot — Bot 3.
Runs all applicable strategy calculators against incoming deals,
persists results to the DB, and surfaces approved deals to the Orchestrator.
"""

from __future__ import annotations
import dataclasses
import logging
from typing import Any, Optional

from realtor_agent.bots.base import BaseBot, BotResult
from realtor_agent.calculations.intake import DealIntake
from realtor_agent.calculations import strategies
from realtor_agent.calculations.rehab_engine import (
    calc_rehab_scope, calc_draw_schedule, ScopeLevel,
)
from realtor_agent.core.models import (
    DealIntakeModel, UnderwritingResultModel, RehabScopeModel, SessionLocal,
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Strategy registry — maps asset type → which calculators to run
# ---------------------------------------------------------------------------

_STRATEGY_MAP: dict[str, list[str]] = {
    "SFR":        ["flip", "wholesale", "brrrr", "rental", "subto", "seller_finance", "wholetail", "novation"],
    "Duplex":     ["brrrr", "rental", "subto", "seller_finance", "multifamily"],
    "4plex":      ["brrrr", "rental", "subto", "seller_finance", "multifamily"],
    "MF":         ["rental", "multifamily", "subto"],
    "Land":       ["land_wholesale", "land_flip_cash", "land_flip_terms", "subdivision"],
    "Commercial": ["rental", "seller_finance"],
}


def _run_strategy(name: str, deal: DealIntake) -> Optional[Any]:
    """Dispatch to the right calculator; return None on skip/error."""
    try:
        if name == "flip":
            return strategies.calc_fix_and_flip(deal)
        if name == "wholetail":
            return strategies.calc_wholetail(deal)
        if name == "wholesale":
            return strategies.calc_wholesale_assignment(deal)
        if name == "novation":
            return strategies.calc_novation(deal)
        if name == "brrrr":
            return strategies.calc_brrrr(deal)
        if name == "rental":
            return strategies.calc_rental_buy_hold(deal)
        if name == "multifamily":
            num_units = {"Duplex": 2, "4plex": 4}.get(deal.asset_type, 4)
            return strategies.calc_small_multifamily(deal, num_units=num_units)
        if name == "subto":
            return strategies.calc_subject_to(deal)
        if name == "seller_finance":
            return strategies.calc_seller_finance(deal)
        if name == "land_wholesale":
            return strategies.calc_land_wholesale(deal)
        if name == "land_flip_cash":
            return strategies.calc_land_flip_cash(deal)
        if name == "land_flip_terms":
            return strategies.calc_land_flip_terms(deal)
        if name == "subdivision":
            return strategies.calc_subdivision_split(deal)
    except Exception as exc:
        logger.warning("Strategy %s failed on deal %s: %s", name, deal.deal_id, exc)
    return None


def _result_to_dict(result: Any) -> dict:
    """Convert a strategy dataclass to a plain dict for JSON storage."""
    if dataclasses.is_dataclass(result):
        return dataclasses.asdict(result)
    return {}


def _scope_level_from_rehab(rehab: float, arv: float) -> ScopeLevel:
    ratio = rehab / arv if arv > 0 else 0
    if ratio < 0.08:
        return ScopeLevel.LIGHT
    if ratio < 0.18:
        return ScopeLevel.MEDIUM
    return ScopeLevel.HEAVY


# ---------------------------------------------------------------------------
# Bot
# ---------------------------------------------------------------------------

class UnderwriterBot(BaseBot):
    """
    Underwriter — runs every applicable strategy calculator and persists results.

    Expects context["web_scout"]["listings"] to be a list of dicts with at
    minimum: deal_id, address, arv (or contract_price + sqft), rehab_cost.

    Returns context key "underwriter" with:
      {
        "results": [per-deal summary],
        "approved": [deals with at least one viable strategy],
        "total": int,
      }
    """

    name = "underwriter"

    def __init__(self, config=None, database=None, **_):
        self.config = config
        self.database = database

    def run(self, context: dict) -> BotResult:
        listings: list[dict] = context.get("web_scout", {}).get("listings", [])

        if not listings:
            logger.info("Underwriter: no listings from web_scout — nothing to underwrite.")
            return BotResult({"results": [], "approved": [], "total": 0})

        db = SessionLocal()
        results = []
        approved = []

        try:
            for raw in listings:
                summary = self._underwrite_one(raw, db)
                results.append(summary)
                if summary.get("viable_strategies"):
                    approved.append(summary)
            db.commit()
        except Exception as exc:
            db.rollback()
            logger.error("Underwriter DB error: %s", exc)
        finally:
            db.close()

        logger.info(
            "Underwriter complete: %d processed, %d approved",
            len(results), len(approved),
        )
        return BotResult({
            "results": results,
            "approved": approved,
            "total": len(results),
            "approved_count": len(approved),
        })

    # ------------------------------------------------------------------

    def _underwrite_one(self, raw: dict, db) -> dict:
        deal = self._build_intake(raw)
        asset = deal.asset_type
        strategy_names = _STRATEGY_MAP.get(asset, _STRATEGY_MAP["SFR"])

        # Determine or fetch existing DB record
        db_record: Optional[DealIntakeModel] = (
            db.query(DealIntakeModel).filter_by(deal_id=deal.deal_id).first()
        )
        if db_record is None:
            db_record = DealIntakeModel(**self._intake_to_model_kwargs(deal))
            db.add(db_record)
            db.flush()

        # Run strategies
        viable_strategies = []
        all_flags: list[str] = []
        best_mao = 0.0
        best_roi = 0.0

        for strat_name in strategy_names:
            result = _run_strategy(strat_name, deal)
            if result is None:
                continue

            payload = _result_to_dict(result)
            viable = getattr(result, "viable", False)
            flags = getattr(result, "flags", [])
            all_flags.extend(flags)

            # Persist result row
            ur = UnderwritingResultModel(
                deal_id_fk=db_record.id,
                strategy=getattr(result, "strategy", strat_name),
                viable=viable,
                flags=flags,
                mao=getattr(result, "mao", None),
                recommended_offer=getattr(result, "recommended_offer", None),
                roi=getattr(result, "roi", None),
                noi=getattr(result, "noi", None),
                cap_rate=getattr(result, "cap_rate", None),
                dscr=getattr(result, "dscr", None),
                coc_return=getattr(result, "coc_return", None),
                annual_cash_flow=getattr(result, "annual_cash_flow", None),
                net_profit=getattr(result, "net_profit", None),
                gross_profit=getattr(result, "gross_profit", None),
                full_result=payload,
            )
            db.add(ur)

            if viable:
                viable_strategies.append(getattr(result, "strategy", strat_name))
                mao = getattr(result, "mao", 0) or 0
                roi = getattr(result, "roi", 0) or 0
                if mao > best_mao:
                    best_mao = mao
                if roi > best_roi:
                    best_roi = roi

        # Rehab scope
        scope = calc_rehab_scope(
            scope_level=_scope_level_from_rehab(deal.rehab_cost, deal.arv),
            sqft=raw.get("sqft", 1200),
        )
        draw = calc_draw_schedule(scope.total)

        db.add(RehabScopeModel(
            deal_id_fk=db_record.id,
            scope_level=scope.scope_level,
            sqft=scope.sqft,
            subtotal=scope.subtotal,
            contingency_pct=scope.contingency_pct,
            contingency_amount=scope.contingency_amount,
            total=scope.total,
            line_items=[dataclasses.asdict(li) for li in scope.line_items],
            draw_schedule=dataclasses.asdict(draw),
        ))

        return {
            "deal_id": deal.deal_id,
            "address": deal.address,
            "asset_type": asset,
            "contract_price": deal.contract_price,
            "arv": deal.arv,
            "rehab_cost": deal.rehab_cost,
            "best_mao": round(best_mao, 2),
            "best_roi": round(best_roi, 4),
            "viable_strategies": viable_strategies,
            "all_flags": list(set(all_flags)),
            "rehab_total": round(scope.total, 2),
        }

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _build_intake(raw: dict) -> DealIntake:
        """Map a raw listing dict (from web_scout) to a DealIntake."""
        sqft = raw.get("sqft") or 1200
        arv = raw.get("arv") or (float(sqft) * 150.0)
        return DealIntake(
            deal_id=str(raw.get("deal_id") or raw.get("property_id") or raw.get("address", "unknown")),
            address=raw.get("address", ""),
            city=raw.get("city", ""),
            state=raw.get("state", ""),
            county=raw.get("county", ""),
            zip_code=str(raw.get("zip") or raw.get("zip_code") or ""),
            asset_type=raw.get("asset_type") or raw.get("property_type") or "SFR",
            contract_price=float(raw.get("contract_price") or raw.get("asking_price") or raw.get("price") or 0),
            arv=float(arv),
            rehab_cost=float(raw.get("rehab_cost") or raw.get("rehab") or arv * 0.10),
            dom=int(raw.get("dom") or 0),
            monthly_rent=float(raw.get("monthly_rent") or raw.get("rent") or 0),
            taxes=float(raw.get("taxes") or 0),
            insurance=float(raw.get("insurance") or 0),
            hoa=float(raw.get("hoa") or 0),
            acres=float(raw.get("acres") or 0),
            zoning=str(raw.get("zoning") or ""),
            buildable=bool(raw.get("buildable", True)),
            road_access=bool(raw.get("road_access", True)),
            flood_zone=str(raw.get("flood_zone") or "X"),
        )

    @staticmethod
    def _intake_to_model_kwargs(deal: DealIntake) -> dict:
        """Extract model column values from a DealIntake."""
        skip = {"_noi"}
        return {
            k: v for k, v in dataclasses.asdict(deal).items()
            if k not in skip
        }
