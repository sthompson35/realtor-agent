"""
DB query layer for the web dashboard.
All functions return plain dicts / lists — no SQLAlchemy objects escape this module.
Falls back to sane zeros when the DB is empty (fresh install).
"""

from __future__ import annotations
from datetime import datetime, timedelta
from sqlalchemy import func, desc
from realtor_agent.core.models import (
    SessionLocal,
    DealIntakeModel,
    UnderwritingResultModel,
    RehabScopeModel,
    ClosedDealModel,
    BotRun,
    OutreachLog,
)


def _session():
    return SessionLocal()


# ---------------------------------------------------------------------------
# Dashboard stats  →  /api/stats
# ---------------------------------------------------------------------------

def get_dashboard_stats() -> dict:
    db = _session()
    try:
        total_deals = db.query(DealIntakeModel).count()
        active_deals = db.query(DealIntakeModel).filter(
            DealIntakeModel.status.in_(["lead", "qualified", "offer_sent", "under_contract"])
        ).count()
        closed_deals = db.query(DealIntakeModel).filter(
            DealIntakeModel.status == "closed"
        ).count()

        # Portfolio value = sum of ARV for active pipeline
        pipeline_value = db.query(func.sum(DealIntakeModel.arv)).filter(
            DealIntakeModel.status.in_(["lead", "qualified", "offer_sent", "under_contract"])
        ).scalar() or 0.0

        # Average deal size (ARV) across all deals
        avg_deal_size = db.query(func.avg(DealIntakeModel.arv)).scalar() or 0.0

        # Closed deal metrics from closed_deals table
        closed_count = db.query(ClosedDealModel).filter(
            ClosedDealModel.status == "Closed"
        ).count()
        total_profit = db.query(func.sum(ClosedDealModel.net_profit)).filter(
            ClosedDealModel.status == "Closed"
        ).scalar() or 0.0
        avg_roi = db.query(func.avg(ClosedDealModel.roi)).filter(
            ClosedDealModel.status == "Closed"
        ).scalar() or 0.0

        # Approved deals (have at least one viable strategy)
        approved_count = db.query(UnderwritingResultModel).filter(
            UnderwritingResultModel.viable == True
        ).distinct(UnderwritingResultModel.deal_id_fk).count()

        # Success rate = closed / (closed + dead) if any completed
        dead_count = db.query(DealIntakeModel).filter(
            DealIntakeModel.status == "dead"
        ).count()
        completed = closed_deals + dead_count
        success_rate = (closed_deals / completed * 100) if completed > 0 else 0.0

        # Monthly revenue (closed deals this month)
        month_start = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        monthly_revenue = db.query(func.sum(ClosedDealModel.net_profit)).filter(
            ClosedDealModel.status == "Closed",
            ClosedDealModel.created_at >= month_start,
        ).scalar() or 0.0

        return {
            "total_deals": total_deals,
            "active_deals": active_deals,
            "closed_deals": closed_deals,
            "pipeline_value": round(pipeline_value, 2),
            "avg_deal_size": round(avg_deal_size, 2),
            "total_profit": round(total_profit, 2),
            "avg_roi": round(avg_roi * 100, 1) if avg_roi else 0.0,
            "approved_deals": approved_count,
            "success_rate": round(success_rate, 1),
            "monthly_revenue": round(monthly_revenue, 2),
        }
    finally:
        db.close()


# ---------------------------------------------------------------------------
# Recent deals  →  /api/deals  (list view)
# ---------------------------------------------------------------------------

def get_deals(
    status: str | None = None,
    limit: int = 50,
    offset: int = 0,
    search: str | None = None,
) -> dict:
    db = _session()
    try:
        q = db.query(DealIntakeModel)
        if status:
            q = q.filter(DealIntakeModel.status == status)
        if search:
            q = q.filter(DealIntakeModel.address.ilike(f"%{search}%"))

        total = q.count()
        rows = q.order_by(desc(DealIntakeModel.created_at)).offset(offset).limit(limit).all()

        deals = []
        for r in rows:
            # Grab best underwriting result
            best = db.query(UnderwritingResultModel).filter(
                UnderwritingResultModel.deal_id_fk == r.id,
                UnderwritingResultModel.viable == True,
            ).order_by(desc(UnderwritingResultModel.roi)).first()

            deals.append({
                "id": r.id,
                "deal_id": r.deal_id,
                "address": r.address,
                "city": r.city,
                "state": r.state,
                "asset_type": r.asset_type,
                "status": r.status,
                "priority": r.priority,
                "contract_price": r.contract_price,
                "arv": r.arv,
                "rehab_cost": r.rehab_cost,
                "monthly_rent": r.monthly_rent,
                "best_strategy": best.strategy if best else None,
                "best_mao": best.mao if best else None,
                "best_roi": round(best.roi * 100, 1) if best and best.roi else None,
                "viable": best is not None,
                "created_at": r.created_at.isoformat() if r.created_at else None,
                "updated_at": r.updated_at.isoformat() if r.updated_at else None,
            })

        return {"deals": deals, "total": total, "offset": offset, "limit": limit}
    finally:
        db.close()


def get_deal(deal_id: int) -> dict | None:
    db = _session()
    try:
        r = db.query(DealIntakeModel).filter(DealIntakeModel.id == deal_id).first()
        if not r:
            return None

        strategies = db.query(UnderwritingResultModel).filter(
            UnderwritingResultModel.deal_id_fk == r.id
        ).order_by(desc(UnderwritingResultModel.viable), desc(UnderwritingResultModel.roi)).all()

        rehab = db.query(RehabScopeModel).filter(
            RehabScopeModel.deal_id_fk == r.id
        ).order_by(desc(RehabScopeModel.created_at)).first()

        return {
            "id": r.id,
            "deal_id": r.deal_id,
            "address": r.address,
            "city": r.city,
            "state": r.state,
            "county": r.county,
            "zip_code": r.zip_code,
            "asset_type": r.asset_type,
            "status": r.status,
            "priority": r.priority,
            "contract_price": r.contract_price,
            "arv": r.arv,
            "rehab_cost": r.rehab_cost,
            "monthly_rent": r.monthly_rent,
            "taxes": r.taxes,
            "insurance": r.insurance,
            "hoa": r.hoa,
            "hold_months": r.hold_months,
            "acres": r.acres,
            "zoning": r.zoning,
            "flood_zone": r.flood_zone,
            "notes": r.notes,
            "created_at": r.created_at.isoformat() if r.created_at else None,
            "strategies": [
                {
                    "strategy": s.strategy,
                    "viable": s.viable,
                    "mao": s.mao,
                    "recommended_offer": s.recommended_offer,
                    "roi": round(s.roi * 100, 1) if s.roi else None,
                    "noi": s.noi,
                    "cap_rate": round(s.cap_rate * 100, 1) if s.cap_rate else None,
                    "dscr": s.dscr,
                    "coc_return": round(s.coc_return * 100, 1) if s.coc_return else None,
                    "net_profit": s.net_profit,
                    "flags": s.flags or [],
                }
                for s in strategies
            ],
            "rehab": {
                "scope_level": rehab.scope_level,
                "sqft": rehab.sqft,
                "subtotal": rehab.subtotal,
                "contingency_pct": rehab.contingency_pct,
                "total": rehab.total,
                "line_items": rehab.line_items,
                "draw_schedule": rehab.draw_schedule,
            } if rehab else None,
        }
    finally:
        db.close()


# ---------------------------------------------------------------------------
# Pipeline stages  →  /api/pipeline
# ---------------------------------------------------------------------------

STAGE_ORDER = ["lead", "qualified", "offer_sent", "under_contract", "closed", "dead"]

def get_pipeline() -> dict:
    db = _session()
    try:
        stages: dict[str, dict] = {}
        for stage in STAGE_ORDER:
            count = db.query(DealIntakeModel).filter(DealIntakeModel.status == stage).count()
            value = db.query(func.sum(DealIntakeModel.arv)).filter(
                DealIntakeModel.status == stage
            ).scalar() or 0.0
            stages[stage] = {"count": count, "value": round(value, 2)}

        # Recent deals per stage (for kanban cards)
        deals_by_stage: dict[str, list] = {s: [] for s in STAGE_ORDER}
        recent = db.query(DealIntakeModel).order_by(
            desc(DealIntakeModel.updated_at)
        ).limit(100).all()

        for r in recent:
            if r.status in deals_by_stage:
                deals_by_stage[r.status].append({
                    "id": r.id,
                    "address": f"{r.address}, {r.city}",
                    "asset_type": r.asset_type,
                    "arv": r.arv,
                    "priority": r.priority,
                    "days_in_stage": (datetime.utcnow() - r.updated_at).days if r.updated_at else 0,
                })

        total_active = sum(
            stages[s]["count"] for s in STAGE_ORDER if s not in ("closed", "dead")
        )

        return {
            "stages": stages,
            "deals_by_stage": deals_by_stage,
            "total_active": total_active,
            "total_closed": stages["closed"]["count"],
        }
    finally:
        db.close()


# ---------------------------------------------------------------------------
# Bot status  →  /api/bots/status
# ---------------------------------------------------------------------------

BOT_NAMES = ["web_scout", "data_clean", "underwriter", "deal_desk",
             "owner_finder", "outreach", "negotiator", "compliance_qa"]

def get_bot_status() -> list[dict]:
    db = _session()
    try:
        bots = []
        for name in BOT_NAMES:
            last_run = db.query(BotRun).filter(
                BotRun.bot_name == name
            ).order_by(desc(BotRun.started_at)).first()

            bots.append({
                "name": name,
                "display_name": name.replace("_", " ").title(),
                "status": last_run.status if last_run else "never_run",
                "last_run": last_run.started_at.isoformat() if last_run and last_run.started_at else None,
                "deals_processed": last_run.deals_processed if last_run else 0,
                "error": last_run.error_message if last_run else None,
            })
        return bots
    finally:
        db.close()


# ---------------------------------------------------------------------------
# Recent activity  →  /api/recent-activity  (sidebar)
# ---------------------------------------------------------------------------

def get_recent_activity(limit: int = 10) -> list[dict]:
    db = _session()
    try:
        activities = []

        # Recent deals
        recent_deals = db.query(DealIntakeModel).order_by(
            desc(DealIntakeModel.created_at)
        ).limit(5).all()
        for d in recent_deals:
            activities.append({
                "icon": "fas fa-home",
                "color": "text-success",
                "message": f"Deal added: {d.address}",
                "timestamp": d.created_at.isoformat() if d.created_at else "",
                "sort_key": d.created_at,
            })

        # Recent bot runs
        recent_bots = db.query(BotRun).order_by(desc(BotRun.started_at)).limit(5).all()
        for b in recent_bots:
            icon = "fas fa-robot"
            color = "text-primary" if b.status == "success" else "text-danger"
            activities.append({
                "icon": icon,
                "color": color,
                "message": f"{b.bot_name} bot: {b.status} ({b.deals_processed or 0} deals)",
                "timestamp": b.started_at.isoformat() if b.started_at else "",
                "sort_key": b.started_at,
            })

        # Recent outreach
        recent_outreach = db.query(OutreachLog).order_by(
            desc(OutreachLog.sent_at)
        ).limit(3).all()
        for o in recent_outreach:
            activities.append({
                "icon": "fas fa-envelope",
                "color": "text-warning",
                "message": f"Outreach sent via {o.channel}",
                "timestamp": o.sent_at.isoformat() if o.sent_at else "",
                "sort_key": o.sent_at,
            })

        # Sort by most recent, remove sort key, return top N
        activities = [
            {k: v for k, v in a.items() if k != "sort_key"}
            for a in sorted(
                activities,
                key=lambda x: x.get("sort_key") or datetime.min,
                reverse=True,
            )[:limit]
        ]

        return activities if activities else [
            {"icon": "fas fa-info-circle", "color": "text-muted",
             "message": "No activity yet — run the pipeline to get started.", "timestamp": ""}
        ]
    finally:
        db.close()


# ---------------------------------------------------------------------------
# System status  →  /api/system-status  (sidebar)
# ---------------------------------------------------------------------------

def get_system_status() -> dict:
    db = _session()
    try:
        # DB health
        db.execute(__import__("sqlalchemy").text("SELECT 1"))
        db_ok = True
    except Exception:
        db_ok = False
    finally:
        db.close()

    active_bots = sum(1 for b in get_bot_status() if b["status"] not in ("never_run", "failed"))
    total_bots = len(BOT_NAMES)

    return {
        "database": {
            "status": "Online" if db_ok else "Offline",
            "badge": "bg-success" if db_ok else "bg-danger",
            "progress": 100 if db_ok else 0,
        },
        "api": {
            "status": "Online",
            "badge": "bg-success",
            "progress": 100,
        },
        "bots": {
            "status": f"{active_bots}/{total_bots}",
            "badge": "bg-success" if active_bots == total_bots else "bg-warning",
            "progress": int(active_bots / total_bots * 100),
        },
    }


# ---------------------------------------------------------------------------
# Analytics  →  /api/analytics
# ---------------------------------------------------------------------------

def get_analytics() -> dict:
    db = _session()
    try:
        # Strategy performance
        strategy_stats = db.query(
            UnderwritingResultModel.strategy,
            func.count(UnderwritingResultModel.id).label("count"),
            func.sum(
                __import__("sqlalchemy").case(
                    (UnderwritingResultModel.viable == True, 1), else_=0
                )
            ).label("viable_count"),
            func.avg(UnderwritingResultModel.roi).label("avg_roi"),
        ).group_by(UnderwritingResultModel.strategy).all()

        strategies = [
            {
                "strategy": r.strategy,
                "analyzed": r.count,
                "viable": r.viable_count,
                "viability_rate": round(r.viable_count / r.count * 100, 1) if r.count else 0,
                "avg_roi": round((r.avg_roi or 0) * 100, 1),
            }
            for r in strategy_stats
        ]

        # Asset type breakdown
        asset_stats = db.query(
            DealIntakeModel.asset_type,
            func.count(DealIntakeModel.id).label("count"),
            func.avg(DealIntakeModel.arv).label("avg_arv"),
        ).group_by(DealIntakeModel.asset_type).all()

        asset_breakdown = [
            {"asset_type": r.asset_type, "count": r.count, "avg_arv": round(r.avg_arv or 0, 2)}
            for r in asset_stats
        ]

        # Closed deal performance from archive
        closed_metrics = db.query(
            func.count(ClosedDealModel.id).label("count"),
            func.sum(ClosedDealModel.net_profit).label("total_profit"),
            func.avg(ClosedDealModel.roi).label("avg_roi"),
            func.avg(ClosedDealModel.hold_months).label("avg_hold"),
        ).filter(ClosedDealModel.status == "Closed").first()

        return {
            "strategy_performance": strategies,
            "asset_breakdown": asset_breakdown,
            "closed_deals": {
                "count": closed_metrics.count or 0,
                "total_profit": round(closed_metrics.total_profit or 0, 2),
                "avg_roi": round((closed_metrics.avg_roi or 0) * 100, 1),
                "avg_hold_months": round(closed_metrics.avg_hold or 0, 1),
            },
        }
    finally:
        db.close()


# ---------------------------------------------------------------------------
# Closed deals (archive)  →  /api/closed-deals
# ---------------------------------------------------------------------------

def get_closed_deals(limit: int = 50) -> list[dict]:
    db = _session()
    try:
        rows = db.query(ClosedDealModel).order_by(
            desc(ClosedDealModel.close_date)
        ).limit(limit).all()
        return [
            {
                "deal_id": r.deal_id,
                "close_date": r.close_date.isoformat() if r.close_date else None,
                "market": r.market,
                "strategy": r.strategy,
                "actual_purchase": r.actual_purchase,
                "actual_rehab": r.actual_rehab,
                "actual_exit": r.actual_exit,
                "equity_in": r.equity_in,
                "hold_months": r.hold_months,
                "gross_profit": r.gross_profit,
                "net_profit": r.net_profit,
                "roi": round((r.roi or 0) * 100, 1),
                "coc": round((r.coc or 0) * 100, 1) if r.coc else None,
                "dscr": r.dscr,
            }
            for r in rows
        ]
    finally:
        db.close()
