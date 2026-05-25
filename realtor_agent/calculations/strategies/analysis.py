"""
Sensitivity_Analysis, Stress_Test, JV_Partnership, Exit_Decision,
Dispo_Calculator, Tax_Estimator.
Source: matching tabs — STLLC_Strategy_Arsenal_Calculator.xlsx
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
from realtor_agent.calculations.intake import DealIntake
from realtor_agent.calculations.strategies.flip import calc_fix_and_flip, FlipResult
from realtor_agent.calculations.strategies.rental import calc_rental_buy_hold, RentalResult


@dataclass
class SensitivityResult:
    strategy: str = "Sensitivity_Analysis"
    base_profit: float = 0.0
    scenarios: list[dict[str, Any]] = field(default_factory=list)
    # Each scenario: {param, delta, profit, roi, viable}


@dataclass
class StressTestResult:
    strategy: str = "Stress_Test"
    base_scenario: dict[str, Any] = field(default_factory=dict)
    stress_scenarios: list[dict[str, Any]] = field(default_factory=list)
    worst_case_profit: float = 0.0
    worst_case_roi: float = 0.0
    viable_under_stress: bool = False


@dataclass
class JVResult:
    strategy: str = "JV_Partnership"
    total_profit: float = 0.0
    money_partner_split_pct: float = 0.0
    operator_split_pct: float = 0.0
    money_partner_return: float = 0.0
    operator_return: float = 0.0
    money_partner_coc: float = 0.0
    viable: bool = False
    flags: list[str] = field(default_factory=list)


@dataclass
class ExitDecisionResult:
    strategy: str = "Exit_Decision"
    flip_profit: float = 0.0
    wholesale_profit: float = 0.0
    rental_coc: float = 0.0
    brrrr_cash_left_in: float = 0.0
    recommended_exit: str = ""
    scores: dict[str, float] = field(default_factory=dict)


@dataclass
class DispoResult:
    strategy: str = "Dispo_Calculator"
    mls_net: float = 0.0
    investor_net: float = 0.0
    auction_net: float = 0.0
    recommended: str = ""
    flags: list[str] = field(default_factory=list)


@dataclass
class TaxEstimateResult:
    strategy: str = "Tax_Estimator"
    gross_profit: float = 0.0
    hold_months: int = 0
    short_term: bool = True         # < 12 months
    federal_rate: float = 0.0
    state_rate: float = 0.0
    se_tax: float = 0.0             # self-employment if dealer
    estimated_tax: float = 0.0
    net_after_tax: float = 0.0
    effective_rate: float = 0.0


# ---------------------------------------------------------------------------
# Sensitivity Analysis
# ---------------------------------------------------------------------------

def calc_sensitivity_analysis(
    deal: DealIntake,
    param_ranges: dict[str, list[float]] | None = None,
) -> SensitivityResult:
    """
    Test how profit changes as key inputs vary ±10 % / ±20 %.

    Default params tested: arv, rehab_cost, monthly_rent.
    """
    if param_ranges is None:
        param_ranges = {
            "arv": [0.80, 0.90, 1.00, 1.10, 1.20],
            "rehab_cost": [0.80, 0.90, 1.00, 1.10, 1.20],
            "monthly_rent": [0.80, 0.90, 1.00, 1.10, 1.20],
        }

    base = calc_fix_and_flip(deal)
    scenarios = []

    for param, multipliers in param_ranges.items():
        for m in multipliers:
            adj = DealIntake(**{
                **deal.__dict__,
                param: getattr(deal, param) * m,
            })
            r = calc_fix_and_flip(adj)
            scenarios.append({
                "param": param,
                "multiplier": m,
                "value": getattr(adj, param),
                "profit": r.net_profit,
                "roi": r.roi,
                "viable": r.viable,
            })

    return SensitivityResult(
        base_profit=base.net_profit,
        scenarios=scenarios,
    )


# ---------------------------------------------------------------------------
# Stress Test
# ---------------------------------------------------------------------------

def calc_stress_test(deal: DealIntake) -> StressTestResult:
    """
    Downside scenario stress testing.

    Stress 1: ARV -10 %, Rehab +15 %
    Stress 2: ARV -20 %, Rehab +25 %
    Stress 3: ARV -30 %, Rehab +40 %  (worst case)
    """
    base = calc_fix_and_flip(deal)

    stress_configs = [
        ("Mild Stress",  -0.10, +0.15),
        ("Moderate Stress", -0.20, +0.25),
        ("Severe Stress", -0.30, +0.40),
    ]

    stress_scenarios = []
    worst_profit = float("inf")
    worst_roi = float("inf")

    for label, arv_delta, rehab_delta in stress_configs:
        adj = DealIntake(**{
            **deal.__dict__,
            "arv": deal.arv * (1 + arv_delta),
            "rehab_cost": deal.rehab_cost * (1 + rehab_delta),
        })
        r = calc_fix_and_flip(adj)
        stress_scenarios.append({
            "label": label,
            "arv_delta_pct": arv_delta,
            "rehab_delta_pct": rehab_delta,
            "profit": r.net_profit,
            "roi": r.roi,
            "viable": r.viable,
        })
        if r.net_profit < worst_profit:
            worst_profit = r.net_profit
            worst_roi = r.roi

    return StressTestResult(
        base_scenario={"profit": base.net_profit, "roi": base.roi},
        stress_scenarios=stress_scenarios,
        worst_case_profit=worst_profit,
        worst_case_roi=worst_roi,
        viable_under_stress=worst_profit > 0,
    )


# ---------------------------------------------------------------------------
# JV Partnership
# ---------------------------------------------------------------------------

def calc_jv_partnership(
    deal: DealIntake,
    total_profit: float,
    equity_contributed: float,
    money_partner_split_pct: float = 0.50,
) -> JVResult:
    """
    Joint Venture return split.

    money_partner_return = total_profit × money_partner_split_pct
    operator_return = total_profit × (1 − split)
    CoC for money partner = money_partner_return / equity_contributed
    """
    op_split = 1 - money_partner_split_pct
    mp_return = total_profit * money_partner_split_pct
    op_return = total_profit * op_split
    mp_coc = mp_return / equity_contributed if equity_contributed > 0 else 0.0

    flags: list[str] = []
    if total_profit <= 0:
        flags.append("NO_PROFIT_TO_SPLIT")
    if mp_coc < 0.15:
        flags.append("MP_COC_BELOW_15PCT")

    return JVResult(
        total_profit=total_profit,
        money_partner_split_pct=money_partner_split_pct,
        operator_split_pct=op_split,
        money_partner_return=mp_return,
        operator_return=op_return,
        money_partner_coc=mp_coc,
        viable=total_profit > 0 and mp_coc >= 0.15,
        flags=flags,
    )


# ---------------------------------------------------------------------------
# Exit Decision
# ---------------------------------------------------------------------------

def calc_exit_decision(deal: DealIntake) -> ExitDecisionResult:
    """
    Compare Flip, Wholesale, Rental, BRRRR side-by-side and recommend best exit.
    Score each strategy 0–100 based on risk-adjusted return.
    """
    from realtor_agent.calculations.strategies.wholesale import calc_wholesale_assignment
    from realtor_agent.calculations.strategies.brrrr import calc_brrrr

    flip = calc_fix_and_flip(deal)
    wholesale = calc_wholesale_assignment(deal)
    rental = calc_rental_buy_hold(deal)
    brrrr = calc_brrrr(deal)

    scores: dict[str, float] = {
        "Flip": (flip.roi * 100) if flip.viable else 0,
        "Wholesale": (wholesale.net_fee / max(deal.contract_price, 1) * 100) if wholesale.viable else 0,
        "Rental": (rental.coc_return * 100) if rental.viable else 0,
        "BRRRR": (brrrr.coc_return * 100) if brrrr.viable else 0,
    }

    recommended = max(scores, key=lambda k: scores[k]) if any(scores.values()) else "None"

    return ExitDecisionResult(
        flip_profit=flip.net_profit,
        wholesale_profit=wholesale.net_fee,
        rental_coc=rental.coc_return,
        brrrr_cash_left_in=brrrr.cash_left_in,
        recommended_exit=recommended,
        scores=scores,
    )


# ---------------------------------------------------------------------------
# Dispo Calculator
# ---------------------------------------------------------------------------

def calc_dispo(
    deal: DealIntake,
    investor_discount_pct: float = 0.15,
    auction_discount_pct: float = 0.20,
) -> DispoResult:
    """
    Disposition strategy comparison: MLS retail vs investor cash vs auction.
    """
    arv = deal.arv
    mls_net = arv - (arv * deal.sell_cost_pct)
    investor_net = arv * (1 - investor_discount_pct) - (arv * 0.01)  # minimal closing
    auction_net = arv * (1 - auction_discount_pct) - (arv * 0.05)   # buyer's premium

    best = max(
        [("MLS", mls_net), ("Investor", investor_net), ("Auction", auction_net)],
        key=lambda x: x[1],
    )

    flags: list[str] = []
    if mls_net < deal.contract_price:
        flags.append("MLS_BELOW_COST")

    return DispoResult(
        mls_net=mls_net,
        investor_net=investor_net,
        auction_net=auction_net,
        recommended=best[0],
        flags=flags,
    )


# ---------------------------------------------------------------------------
# Tax Estimator
# ---------------------------------------------------------------------------

def calc_tax_estimate(
    gross_profit: float,
    hold_months: int,
    federal_lt_rate: float = 0.20,
    federal_st_rate: float = 0.37,
    state_rate: float = 0.05,
    is_dealer: bool = False,
) -> TaxEstimateResult:
    """
    Rough tax impact estimate.

    Short-term (< 12 months): ordinary income rates apply.
    Long-term (≥ 12 months): capital gains rates apply.
    Dealer status: add SE tax (~15.3 %) on top of ordinary income rate.
    """
    short_term = hold_months < 12
    federal_rate = federal_st_rate if short_term else federal_lt_rate
    se_tax = gross_profit * 0.153 if is_dealer else 0.0
    estimated_tax = gross_profit * (federal_rate + state_rate) + se_tax
    net_after = gross_profit - estimated_tax
    effective_rate = estimated_tax / gross_profit if gross_profit > 0 else 0.0

    return TaxEstimateResult(
        gross_profit=gross_profit,
        hold_months=hold_months,
        short_term=short_term,
        federal_rate=federal_rate,
        state_rate=state_rate,
        se_tax=se_tax,
        estimated_tax=estimated_tax,
        net_after_tax=net_after,
        effective_rate=effective_rate,
    )
