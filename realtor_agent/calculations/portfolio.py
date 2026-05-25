"""
Portfolio metrics — matches formulas in:
  closed_deals_archive_companion_v8.xlsx  (10_CLOSED_DEALS_LOG)
  portfolio_rollup_master_v8.xlsx         (02_PORTFOLIO_DASHBOARD, 03_STRATEGY_ROLLUP)

All functions are pure; call them on lists of ClosedDeal dicts or dataclasses.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date
from typing import Optional


# ---------------------------------------------------------------------------
# Closed Deal record (mirrors 10_CLOSED_DEALS_LOG columns)
# ---------------------------------------------------------------------------

@dataclass
class ClosedDeal:
    deal_id: str
    close_date: Optional[date]
    exit_date: Optional[date]
    market: str
    strategy: str
    entity: str
    status: str                         # Closed | Cancelled | etc.

    # Projected
    proj_purchase: float = 0.0
    proj_rehab: float = 0.0
    proj_exit: float = 0.0
    proj_rent: float = 0.0

    # Actual
    actual_purchase: float = 0.0
    actual_rehab: float = 0.0
    actual_exit: float = 0.0
    actual_rent: float = 0.0

    # Financing
    debt_proceeds: float = 0.0         # Total debt raised for this deal
    equity_in: float = 0.0             # Cash / equity invested

    hold_months: int = 0


# ---------------------------------------------------------------------------
# Per-deal computed metrics (mirrors archive dashboard formulas)
# ---------------------------------------------------------------------------

@dataclass
class DealMetrics:
    deal_id: str
    gross_profit: float             # actual_exit - actual_purchase - actual_rehab
    net_profit: float               # gross_profit (all costs already in actuals)
    roi: float                      # net_profit / equity_in
    coc: float                      # annual_cash_flow / equity_in (for rentals)
    dscr: float                     # noi / annual_debt_service
    proj_vs_actual_purchase: float  # variance %
    proj_vs_actual_rehab: float
    proj_vs_actual_exit: float


def calc_deal_metrics(deal: ClosedDeal, annual_noi: float = 0.0, annual_debt_service: float = 0.0) -> DealMetrics:
    """
    Compute per-deal performance metrics.

    gross_profit = actual_exit - actual_purchase - actual_rehab
    roi          = net_profit / equity_in
    coc          = (annual_noi - annual_debt_service) / equity_in   [rental/BRRRR]
    dscr         = annual_noi / annual_debt_service
    """
    gross = deal.actual_exit - deal.actual_purchase - deal.actual_rehab
    net = gross  # debt proceeds tracked separately in portfolio rollup

    equity = max(deal.equity_in, 1.0)
    roi = net / equity

    annual_cf = annual_noi - annual_debt_service
    coc = annual_cf / equity if annual_noi > 0 else 0.0
    dscr = annual_noi / annual_debt_service if annual_debt_service > 0 else 0.0

    def variance(proj, actual):
        return (actual - proj) / proj if proj else 0.0

    return DealMetrics(
        deal_id=deal.deal_id,
        gross_profit=gross,
        net_profit=net,
        roi=roi,
        coc=coc,
        dscr=dscr,
        proj_vs_actual_purchase=variance(deal.proj_purchase, deal.actual_purchase),
        proj_vs_actual_rehab=variance(deal.proj_rehab, deal.actual_rehab),
        proj_vs_actual_exit=variance(deal.proj_exit, deal.actual_exit),
    )


# ---------------------------------------------------------------------------
# Portfolio Dashboard (02_PORTFOLIO_DASHBOARD)
# ---------------------------------------------------------------------------

@dataclass
class PortfolioDashboard:
    total_deals: int
    closed_deals: int
    active_deals: int
    total_equity_deployed: float
    total_gross_profit: float
    total_net_profit: float
    avg_roi: float
    avg_hold_months: float
    avg_gross_profit: float
    best_deal_roi: float
    worst_deal_roi: float
    total_pipeline_value: float


def calc_portfolio_dashboard(
    closed_deals: list[ClosedDeal],
    metrics: list[DealMetrics],
    active_pipeline_value: float = 0.0,
    active_deal_count: int = 0,
) -> PortfolioDashboard:
    """Aggregate closed deal metrics into a fund-level dashboard."""
    closed = [d for d in closed_deals if d.status.lower() == "closed"]
    n = len(closed)

    total_equity = sum(d.equity_in for d in closed)
    total_gross = sum(m.gross_profit for m in metrics)
    total_net = sum(m.net_profit for m in metrics)
    rois = [m.roi for m in metrics if m.roi != 0]
    avg_roi = sum(rois) / len(rois) if rois else 0.0
    hold_months = [d.hold_months for d in closed if d.hold_months > 0]
    avg_hold = sum(hold_months) / len(hold_months) if hold_months else 0.0

    return PortfolioDashboard(
        total_deals=n + active_deal_count,
        closed_deals=n,
        active_deals=active_deal_count,
        total_equity_deployed=total_equity,
        total_gross_profit=total_gross,
        total_net_profit=total_net,
        avg_roi=avg_roi,
        avg_hold_months=avg_hold,
        avg_gross_profit=total_gross / n if n else 0.0,
        best_deal_roi=max(rois) if rois else 0.0,
        worst_deal_roi=min(rois) if rois else 0.0,
        total_pipeline_value=active_pipeline_value,
    )


# ---------------------------------------------------------------------------
# Strategy Rollup (03_STRATEGY_ROLLUP)
# ---------------------------------------------------------------------------

@dataclass
class StrategyRollup:
    strategy: str
    deal_count: int
    total_profit: float
    avg_roi: float
    avg_hold_months: float


def calc_strategy_rollup(
    closed_deals: list[ClosedDeal],
    metrics: list[DealMetrics],
) -> list[StrategyRollup]:
    """Group closed deals by strategy and compute per-strategy KPIs."""
    from collections import defaultdict

    metrics_by_id = {m.deal_id: m for m in metrics}
    groups: dict[str, list[tuple[ClosedDeal, DealMetrics]]] = defaultdict(list)

    for deal in closed_deals:
        if deal.deal_id in metrics_by_id:
            groups[deal.strategy].append((deal, metrics_by_id[deal.deal_id]))

    rollups: list[StrategyRollup] = []
    for strategy, pairs in sorted(groups.items()):
        profits = [m.net_profit for _, m in pairs]
        rois = [m.roi for _, m in pairs]
        holds = [d.hold_months for d, _ in pairs if d.hold_months > 0]
        rollups.append(StrategyRollup(
            strategy=strategy,
            deal_count=len(pairs),
            total_profit=sum(profits),
            avg_roi=sum(rois) / len(rois) if rois else 0.0,
            avg_hold_months=sum(holds) / len(holds) if holds else 0.0,
        ))

    return rollups


# ---------------------------------------------------------------------------
# Market Rollup (05_MARKET_ROLLUP)
# ---------------------------------------------------------------------------

@dataclass
class MarketRollup:
    market: str
    deal_count: int
    total_profit: float
    avg_roi: float


def calc_market_rollup(
    closed_deals: list[ClosedDeal],
    metrics: list[DealMetrics],
) -> list[MarketRollup]:
    """Group closed deals by market (city/MSA) and compute KPIs."""
    from collections import defaultdict

    metrics_by_id = {m.deal_id: m for m in metrics}
    groups: dict[str, list[DealMetrics]] = defaultdict(list)

    for deal in closed_deals:
        if deal.deal_id in metrics_by_id:
            groups[deal.market].append(metrics_by_id[deal.deal_id])

    rollups: list[MarketRollup] = []
    for market, mlist in sorted(groups.items()):
        profits = [m.net_profit for m in mlist]
        rois = [m.roi for m in mlist]
        rollups.append(MarketRollup(
            market=market,
            deal_count=len(mlist),
            total_profit=sum(profits),
            avg_roi=sum(rois) / len(rois) if rois else 0.0,
        ))

    return rollups
