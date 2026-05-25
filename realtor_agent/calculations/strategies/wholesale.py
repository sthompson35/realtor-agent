"""
Wholesale_Assignment + Novation calculators.
Source: Wholesale_Assignment tab, Novation tab — STLLC_Strategy_Arsenal_Calculator.xlsx
"""

from __future__ import annotations
from dataclasses import dataclass
from realtor_agent.calculations.intake import DealIntake


@dataclass
class WholesaleResult:
    strategy: str
    contract_price: float       # What we put the property under contract for
    investor_mao: float         # Max an end-buyer investor would pay
    assignment_fee: float       # Spread = investor_mao - contract_price
    min_fee: float              # Floor from Settings
    net_fee: float              # max(assignment_fee, min_fee)
    viable: bool
    flags: list[str]


@dataclass
class NovationResult:
    strategy: str
    arv: float
    sell_cost: float
    seller_net: float           # contract_price = what seller needs
    gross_remainder: float      # ARV - sell_cost - seller_net
    investor_split: float       # investor share of remainder
    seller_split: float         # seller's bonus share
    net_to_investor: float
    viable: bool
    flags: list[str]


def calc_wholesale_assignment(deal: DealIntake) -> WholesaleResult:
    """
    Wholesale / Assignment fee.

    The investor's MAO (what a fix-and-flip buyer would pay) is calculated
    using the flip formula; we subtract our contract price to get our fee.

    investor_MAO = ARV × (1 - sell_cost_pct - investor_margin_pct) - Rehab - HoldingCosts
    AssignmentFee = investor_MAO - contract_price
    """
    arv = deal.arv
    rehab = deal.rehab_cost

    hold_months = deal.hold_months
    holding = arv * 0.01 * hold_months
    sell = arv * deal.sell_cost_pct
    investor_profit = arv * deal.investor_margin_pct

    investor_mao = arv - rehab - holding - sell - investor_profit

    assignment_fee = investor_mao - deal.contract_price
    net_fee = max(assignment_fee, deal.wholesale_min_fee)

    flags: list[str] = []
    if assignment_fee < deal.wholesale_min_fee:
        flags.append("FEE_BELOW_MINIMUM")
    if investor_mao <= deal.contract_price:
        flags.append("NO_SPREAD")
    if deal.contract_price > arv * 0.70:
        flags.append("HIGH_ACQUISITION_RATIO")

    return WholesaleResult(
        strategy="Wholesale_Assignment",
        contract_price=deal.contract_price,
        investor_mao=investor_mao,
        assignment_fee=assignment_fee,
        min_fee=deal.wholesale_min_fee,
        net_fee=net_fee,
        viable=assignment_fee >= deal.wholesale_min_fee,
        flags=flags,
    )


def calc_novation(
    deal: DealIntake,
    investor_split_pct: float = 0.50,
    agent_commission_pct: float = 0.06,
) -> NovationResult:
    """
    Novation — we list and sell the seller's property at retail; profit is split.

    Investor nets: (ARV - agent_commission - seller_net) × investor_split_pct
    """
    arv = deal.arv
    sell_cost = arv * (agent_commission_pct + deal.buy_close_pct)
    seller_net = deal.contract_price   # what the seller must walk away with

    gross_remainder = arv - sell_cost - seller_net
    investor_share = gross_remainder * investor_split_pct
    seller_share = gross_remainder * (1 - investor_split_pct)

    flags: list[str] = []
    if gross_remainder <= 0:
        flags.append("NO_REMAINDER")
    if investor_share < deal.wholesale_min_fee:
        flags.append("PROFIT_BELOW_MINIMUM")

    return NovationResult(
        strategy="Novation",
        arv=arv,
        sell_cost=sell_cost,
        seller_net=seller_net,
        gross_remainder=gross_remainder,
        investor_split=investor_share,
        seller_split=seller_share,
        net_to_investor=investor_share,
        viable=investor_share >= deal.wholesale_min_fee,
        flags=flags,
    )
