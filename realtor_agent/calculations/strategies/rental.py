"""
Rental_BuyHold + Small_Multifamily calculators.
Source: Rental_BuyHold tab, Small_Multifamily tab — STLLC_Strategy_Arsenal_Calculator.xlsx
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from realtor_agent.calculations.intake import DealIntake
from realtor_agent.calculations._math import pmt


@dataclass
class RentalResult:
    strategy: str
    gross_annual_rent: float
    vacancy_loss: float
    effective_gross_income: float
    operating_expenses: float
    noi: float
    cap_rate: float             # NOI / (purchase + rehab)
    monthly_payment: float
    annual_debt_service: float
    annual_cash_flow: float
    dscr: float
    coc_return: float           # annual_cash_flow / equity_in
    equity_in: float            # down + buy_close + rehab
    grm: float                  # Gross Rent Multiplier = price / gross_annual_rent
    mao_at_cap: float           # purchase price that hits target cap rate
    viable: bool
    flags: list[str]


@dataclass
class MultifamilyResult:
    strategy: str
    num_units: int
    gross_annual_rent: float
    vacancy_loss: float
    effective_gross_income: float
    operating_expenses: float
    noi: float
    cap_rate: float
    monthly_payment: float
    annual_debt_service: float
    annual_cash_flow: float
    dscr: float
    coc_return: float
    equity_in: float
    grm: float
    price_per_unit: float
    noi_per_unit: float
    viable: bool
    flags: list[str]


def calc_rental_buy_hold(
    deal: DealIntake,
    target_cap_rate: float = 0.08,
    target_coc: float = 0.08,
) -> RentalResult:
    """
    Single-family / small rental buy-and-hold underwriting.

    Cap rate = NOI / (purchase + rehab)
    DSCR = NOI / annual_debt_service
    CoC = annual_cash_flow / equity_in
    MAO at target cap = (NOI / target_cap_rate) - rehab
    """
    gross = deal.gross_annual_rent
    vacancy = gross * deal.vacancy_pct
    egi = gross - vacancy
    opex = deal.annual_operating_expenses
    noi = egi - opex

    total_invested = deal.contract_price + deal.rehab_cost
    cap_rate = noi / total_invested if total_invested > 0 else 0.0

    loan = deal.loan_amount
    monthly_pmt = pmt(deal.rate, deal.term_years, loan)
    ads = monthly_pmt * 12
    acf = noi - ads
    dscr = noi / ads if ads > 0 else 0.0

    equity_in = deal.down_payment + deal.buy_closing_cost + deal.rehab_cost
    coc = acf / equity_in if equity_in > 0 else 0.0

    grm = deal.contract_price / gross if gross > 0 else 0.0
    mao_at_cap = (noi / target_cap_rate) - deal.rehab_cost if target_cap_rate > 0 else 0.0

    flags: list[str] = []
    if noi < 0:
        flags.append("NEGATIVE_NOI")
    if dscr < 1.0:
        flags.append("NEGATIVE_DSCR")
    if dscr < 1.25:
        flags.append("DSCR_BELOW_1.25")
    if coc < target_coc:
        flags.append(f"COC_BELOW_{int(target_coc*100)}PCT")
    if cap_rate < target_cap_rate:
        flags.append(f"CAP_BELOW_{int(target_cap_rate*100)}PCT")
    if deal.contract_price > mao_at_cap:
        flags.append("OVER_MAO_AT_CAP")

    return RentalResult(
        strategy="Rental_BuyHold",
        gross_annual_rent=gross,
        vacancy_loss=vacancy,
        effective_gross_income=egi,
        operating_expenses=opex,
        noi=noi,
        cap_rate=cap_rate,
        monthly_payment=monthly_pmt,
        annual_debt_service=ads,
        annual_cash_flow=acf,
        dscr=dscr,
        coc_return=coc,
        equity_in=equity_in,
        grm=grm,
        mao_at_cap=mao_at_cap,
        viable=dscr >= 1.25 and coc >= target_coc,
        flags=flags,
    )


def calc_small_multifamily(
    deal: DealIntake,
    num_units: int = 4,
    unit_rents: Optional[list[float]] = None,
    opex_ratio: float = 0.40,
    target_cap_rate: float = 0.07,
) -> MultifamilyResult:
    """
    Small multifamily (2–20 units) underwriting.
    If unit_rents not provided, uses deal.monthly_rent × num_units.
    opex_ratio: fraction of EGI consumed by operating expenses (typical 35–45%).
    """
    if unit_rents:
        monthly_total = sum(unit_rents)
    else:
        monthly_total = deal.monthly_rent * num_units

    gross = monthly_total * 12
    vacancy = gross * deal.vacancy_pct
    egi = gross - vacancy
    opex = egi * opex_ratio
    noi = egi - opex

    total_invested = deal.contract_price + deal.rehab_cost
    cap_rate = noi / total_invested if total_invested > 0 else 0.0

    loan = deal.loan_amount
    monthly_pmt = pmt(deal.rate, deal.term_years, loan)
    ads = monthly_pmt * 12
    acf = noi - ads
    dscr = noi / ads if ads > 0 else 0.0

    equity_in = deal.down_payment + deal.buy_closing_cost + deal.rehab_cost
    coc = acf / equity_in if equity_in > 0 else 0.0

    grm = deal.contract_price / gross if gross > 0 else 0.0
    price_per_unit = deal.contract_price / num_units
    noi_per_unit = noi / num_units

    flags: list[str] = []
    if dscr < 1.25:
        flags.append("DSCR_BELOW_1.25")
    if cap_rate < target_cap_rate:
        flags.append(f"CAP_BELOW_{int(target_cap_rate*100)}PCT")
    if noi < 0:
        flags.append("NEGATIVE_NOI")

    return MultifamilyResult(
        strategy="Small_Multifamily",
        num_units=num_units,
        gross_annual_rent=gross,
        vacancy_loss=vacancy,
        effective_gross_income=egi,
        operating_expenses=opex,
        noi=noi,
        cap_rate=cap_rate,
        monthly_payment=monthly_pmt,
        annual_debt_service=ads,
        annual_cash_flow=acf,
        dscr=dscr,
        coc_return=coc,
        equity_in=equity_in,
        grm=grm,
        price_per_unit=price_per_unit,
        noi_per_unit=noi_per_unit,
        viable=dscr >= 1.25 and cap_rate >= target_cap_rate,
        flags=flags,
    )
