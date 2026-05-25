"""
Option_Control + Subdivision_Split calculators.
Source: Option_Control tab, Subdivision_Split tab — STLLC_Strategy_Arsenal_Calculator.xlsx
"""

from __future__ import annotations
from dataclasses import dataclass
from realtor_agent.calculations.intake import DealIntake


@dataclass
class OptionResult:
    strategy: str
    option_fee: float               # Non-refundable consideration paid
    strike_price: float             # Price at which we can buy
    market_value: float             # ARV / current FMV
    sell_cost: float                # Cost to exit / assign
    gross_profit: float             # market_value - strike - sell_cost
    net_profit: float               # gross_profit - option_fee
    roi: float                      # net_profit / option_fee
    viable: bool
    flags: list[str]


@dataclass
class SubdivisionResult:
    strategy: str
    total_acres: float
    num_parcels: int
    total_buy_cost: float           # purchase + closing
    cost_per_parcel: float
    sell_price_per_parcel: float
    sell_cost_per_parcel: float
    net_per_parcel: float
    total_net_profit: float
    roi: float
    viable: bool
    flags: list[str]


def calc_option_control(
    deal: DealIntake,
    option_fee: float = 1000.0,
    strike_price: float = 0.0,
) -> OptionResult:
    """
    Option / Control — we control the property via an option agreement.

    Profit = (market_value − strike) − sell_cost − option_fee
    ROI is calculated on option_fee (our risk capital).
    """
    market_value = deal.arv
    strike = strike_price or deal.contract_price
    sell_cost = market_value * deal.sell_cost_pct

    gross_profit = market_value - strike - sell_cost
    net_profit = gross_profit - option_fee
    roi = net_profit / option_fee if option_fee > 0 else 0.0

    flags: list[str] = []
    if net_profit <= 0:
        flags.append("NO_PROFIT")
    if strike > market_value:
        flags.append("STRIKE_ABOVE_MARKET")
    if roi < 2.0:
        flags.append("LOW_ROI_ON_OPTION")

    return OptionResult(
        strategy="Option_Control",
        option_fee=option_fee,
        strike_price=strike,
        market_value=market_value,
        sell_cost=sell_cost,
        gross_profit=gross_profit,
        net_profit=net_profit,
        roi=roi,
        viable=net_profit > 0,
        flags=flags,
    )


def calc_subdivision_split(
    deal: DealIntake,
    num_parcels: int = 2,
    sell_price_per_parcel: float = 0.0,
    soft_costs_per_parcel: float = 2500.0,  # permits, survey, engineering
) -> SubdivisionResult:
    """
    Subdivision / parcel split — buy large parcel, split, sell individually.

    cost_per_parcel = (purchase + closing) / num_parcels + soft_costs
    net_per_parcel  = sell_price - sell_closing - cost_per_parcel
    """
    total_buy = deal.contract_price + deal.buy_closing_cost
    cost_per = (total_buy / num_parcels) + soft_costs_per_parcel

    sp = sell_price_per_parcel or (deal.arv / num_parcels)
    sell_close = sp * deal.sell_cost_pct
    net_per = sp - sell_close - cost_per
    total_net = net_per * num_parcels

    roi = total_net / total_buy if total_buy > 0 else 0.0

    flags: list[str] = []
    if net_per <= 0:
        flags.append("NO_PROFIT_PER_PARCEL")
    if roi < 0.20:
        flags.append("LOW_ROI")
    if deal.acres / num_parcels < 1.0:
        flags.append("SMALL_PARCEL_SIZE")

    return SubdivisionResult(
        strategy="Subdivision_Split",
        total_acres=deal.acres,
        num_parcels=num_parcels,
        total_buy_cost=total_buy,
        cost_per_parcel=cost_per,
        sell_price_per_parcel=sp,
        sell_cost_per_parcel=sell_close,
        net_per_parcel=net_per,
        total_net_profit=total_net,
        roi=roi,
        viable=net_per > 0 and roi >= 0.20,
        flags=flags,
    )
