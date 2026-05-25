"""
Fix_and_Flip + Wholetail calculators.
Source: Fix_and_Flip tab, Wholetail tab — STLLC_Strategy_Arsenal_Calculator.xlsx
"""

from __future__ import annotations
from dataclasses import dataclass
from realtor_agent.calculations.intake import DealIntake
from realtor_agent.calculations._math import pmt


@dataclass
class FlipResult:
    strategy: str
    arv: float
    contract_price: float
    rehab_cost: float
    holding_costs: float
    selling_costs: float
    buy_closing_costs: float
    financing_costs: float
    total_costs: float          # rehab + hold + sell + close + financing
    total_in: float             # contract + total_costs
    gross_profit: float         # ARV - total_in
    net_profit: float           # gross_profit (alias; financing already included)
    roi: float                  # net_profit / total_in
    mao: float                  # Maximum Allowable Offer at target profit
    recommended_offer: float    # MAO * 0.95 — negotiation buffer
    viable: bool
    flags: list[str]


def calc_fix_and_flip(deal: DealIntake) -> FlipResult:
    """
    Fix & Flip MAO (Missouri-safe underwriting).

    MAO = ARV
          - Rehab
          - Holding costs  (ARV × hold_pct × hold_months)
          - Selling costs  (ARV × sell_cost_pct)
          - Buy closing    (MAO × buy_close_pct)  [iterative; approx as contract × pct]
          - Financing      (loan × points + monthly_pmt × hold_months)
          - Target profit  (ARV × flip_profit_target_pct)
    """
    arv = deal.arv
    rehab = deal.rehab_cost
    hold_months = deal.hold_months

    holding = arv * 0.01 * hold_months          # 1 % of ARV / month
    selling = arv * deal.sell_cost_pct
    profit = arv * deal.flip_profit_target_pct

    # Loan assumed on contract price (hard-money style); points + interest
    loan = deal.contract_price * (1 - deal.down_pct)
    points_cost = loan * deal.points
    monthly_payment = pmt(deal.rate, deal.term_years, loan)
    interest_cost = monthly_payment * hold_months

    buy_close = deal.contract_price * deal.buy_close_pct

    total_costs = rehab + holding + selling + buy_close + points_cost + interest_cost + profit
    mao = arv - total_costs

    # Evaluate at contract price
    total_in = deal.contract_price + rehab + holding + selling + buy_close + points_cost + interest_cost
    gross_profit = arv - total_in
    roi = gross_profit / total_in if total_in > 0 else 0.0

    flags: list[str] = []
    if mao <= 0:
        flags.append("NEGATIVE_MAO")
    if rehab > arv * 0.25:
        flags.append("HIGH_REHAB_RATIO")
    if roi < 0.15:
        flags.append("LOW_ROI")
    if deal.contract_price > mao:
        flags.append("OVER_MAO")

    return FlipResult(
        strategy="Fix_and_Flip",
        arv=arv,
        contract_price=deal.contract_price,
        rehab_cost=rehab,
        holding_costs=holding,
        selling_costs=selling,
        buy_closing_costs=buy_close,
        financing_costs=points_cost + interest_cost,
        total_costs=total_costs - profit,
        total_in=total_in,
        gross_profit=gross_profit,
        net_profit=gross_profit,
        roi=roi,
        mao=mao,
        recommended_offer=mao * 0.95,
        viable=len(flags) == 0,
        flags=flags,
    )


def calc_wholetail(deal: DealIntake, light_rehab_override: float | None = None) -> FlipResult:
    """
    Wholetail — light cosmetic rehab then retail list.
    Same math as flip but rehab is capped at a light-touch amount (~5 % of ARV).
    """
    light = light_rehab_override or min(deal.rehab_cost, deal.arv * 0.05)
    modified = DealIntake(**{**deal.__dict__, "rehab_cost": light, "hold_months": max(deal.hold_months, 2)})
    result = calc_fix_and_flip(modified)
    result.strategy = "Wholetail"
    return result
