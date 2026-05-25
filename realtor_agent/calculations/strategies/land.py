"""
Land_Wholesale, Land_Flip_Cash, Land_Flip_Terms calculators.
Source: Land_Wholesale, Land_Flip_Cash, Land_Flip_Terms tabs — STLLC_Strategy_Arsenal_Calculator.xlsx

Kill-switch flags (from Land_Wholesale tab):
  • not buildable  → KILL_NOT_BUILDABLE
  • no road access → KILL_NO_ACCESS
  • flood zone AE/VE → KILL_FLOOD_ZONE
"""

from __future__ import annotations
from dataclasses import dataclass
from realtor_agent.calculations.intake import DealIntake
from realtor_agent.calculations._math import pmt


@dataclass
class LandWholesaleResult:
    strategy: str
    contract_price: float
    investor_mao: float
    assignment_fee: float
    kill_switch_triggered: bool
    kill_reasons: list[str]
    viable: bool
    flags: list[str]


@dataclass
class LandFlipCashResult:
    strategy: str
    buy_price: float
    sell_price: float
    buy_closing: float
    sell_closing: float
    total_cost: float
    gross_profit: float
    roi: float
    viable: bool
    flags: list[str]


@dataclass
class LandFlipTermsResult:
    strategy: str
    sell_price: float
    down_payment_received: float
    loan_amount_to_buyer: float
    rate: float
    term_years: int
    monthly_payment_received: float
    total_received: float           # down + all monthly payments
    buy_price: float
    net_profit: float
    yield_pct: float
    viable: bool
    flags: list[str]


def _land_kill_flags(deal: DealIntake) -> list[str]:
    reasons = []
    if not deal.buildable:
        reasons.append("KILL_NOT_BUILDABLE")
    if not deal.road_access:
        reasons.append("KILL_NO_ACCESS")
    if deal.flood_zone.upper() in ("AE", "VE"):
        reasons.append("KILL_FLOOD_ZONE")
    return reasons


def calc_land_wholesale(
    deal: DealIntake,
    price_per_acre_investor: float = 0.0,
) -> LandWholesaleResult:
    """
    Land wholesale assignment.

    investor_MAO = acres × price_per_acre_investor (or ARV if per-acre not given)
    AssignmentFee = investor_MAO - contract_price
    Kill-switches abort the deal outright.
    """
    kill_reasons = _land_kill_flags(deal)
    kill_triggered = len(kill_reasons) > 0

    investor_mao = (deal.acres * price_per_acre_investor) if price_per_acre_investor else deal.arv
    assignment_fee = investor_mao - deal.contract_price

    flags = list(kill_reasons)
    if not kill_triggered and assignment_fee < deal.wholesale_min_fee:
        flags.append("FEE_BELOW_MINIMUM")

    return LandWholesaleResult(
        strategy="Land_Wholesale",
        contract_price=deal.contract_price,
        investor_mao=investor_mao,
        assignment_fee=assignment_fee,
        kill_switch_triggered=kill_triggered,
        kill_reasons=kill_reasons,
        viable=not kill_triggered and assignment_fee >= deal.wholesale_min_fee,
        flags=flags,
    )


def calc_land_flip_cash(deal: DealIntake) -> LandFlipCashResult:
    """
    Land flip for cash — buy low, sell retail.

    Profit = sell_price - buy_price - buy_closing - sell_closing
    """
    kill_reasons = _land_kill_flags(deal)

    buy = deal.contract_price
    sell = deal.arv
    buy_close = deal.buy_closing_cost
    sell_close = sell * deal.sell_cost_pct
    total_cost = buy + buy_close
    gross_profit = sell - sell_close - total_cost
    roi = gross_profit / total_cost if total_cost > 0 else 0.0

    flags = list(kill_reasons)
    if gross_profit <= 0:
        flags.append("NO_PROFIT")
    if roi < 0.20:
        flags.append("LOW_ROI")

    return LandFlipCashResult(
        strategy="Land_Flip_Cash",
        buy_price=buy,
        sell_price=sell,
        buy_closing=buy_close,
        sell_closing=sell_close,
        total_cost=total_cost,
        gross_profit=gross_profit,
        roi=roi,
        viable=not kill_reasons and gross_profit > 0 and roi >= 0.20,
        flags=flags,
    )


def calc_land_flip_terms(
    deal: DealIntake,
    buyer_down_pct: float = 0.10,
    sell_price: float = 0.0,
    note_rate: float = 0.10,
    note_term_years: int = 10,
) -> LandFlipTermsResult:
    """
    Land flip with owner-carry note to buyer.

    We sell at sell_price (defaults to ARV), collect down + monthly payments.
    yield = total_received / (buy_price + buy_closing) - 1
    """
    kill_reasons = _land_kill_flags(deal)

    sp = sell_price or deal.arv
    down_received = sp * buyer_down_pct
    loan_to_buyer = sp - down_received

    monthly_received = pmt(note_rate, note_term_years, loan_to_buyer)
    total_received = down_received + monthly_received * note_term_years * 12

    buy_total = deal.contract_price + deal.buy_closing_cost
    net_profit = total_received - buy_total
    yield_pct = net_profit / buy_total if buy_total > 0 else 0.0

    flags = list(kill_reasons)
    if net_profit <= 0:
        flags.append("NO_PROFIT")

    return LandFlipTermsResult(
        strategy="Land_Flip_Terms",
        sell_price=sp,
        down_payment_received=down_received,
        loan_amount_to_buyer=loan_to_buyer,
        rate=note_rate,
        term_years=note_term_years,
        monthly_payment_received=monthly_received,
        total_received=total_received,
        buy_price=deal.contract_price,
        net_profit=net_profit,
        yield_pct=yield_pct,
        viable=not kill_reasons and net_profit > 0,
        flags=flags,
    )
