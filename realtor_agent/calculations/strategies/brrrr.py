"""
BRRRR calculator — Buy, Rehab, Rent, Refinance, Repeat.
Source: BRRRR tab — STLLC_Strategy_Arsenal_Calculator.xlsx
"""

from __future__ import annotations
from dataclasses import dataclass
from realtor_agent.calculations.intake import DealIntake
from realtor_agent.calculations._math import pmt


@dataclass
class BRRRRResult:
    strategy: str
    # Phase 1 — Acquisition
    purchase_price: float
    rehab_cost: float
    buy_closing: float
    total_cash_in: float        # purchase + rehab + closing (pre-refi)

    # Phase 2 — Rental income
    noi: float                  # annual

    # Phase 3 — Refinance
    arv: float
    refi_ltv: float
    refi_loan: float
    refi_proceeds: float        # refi_loan - any existing acquisition debt
    cash_left_in: float         # total_cash_in - refi_proceeds

    # Phase 4 — Stabilized metrics
    monthly_refi_payment: float
    annual_debt_service: float
    annual_cash_flow: float
    dscr: float
    coc_return: float           # annual_cash_flow / cash_left_in
    equity_created: float       # arv - refi_loan
    viable: bool
    flags: list[str]


def calc_brrrr(
    deal: DealIntake,
    refi_ltv: float = 0.75,
    refi_rate: float | None = None,
    refi_term_years: int = 30,
    existing_debt: float = 0.0,
) -> BRRRRResult:
    """
    BRRRR underwriting.

    Phase 1 assumes all-cash or hard-money acquisition (costs = purchase + rehab + closing).
    Phase 3 refinances at refi_ltv × ARV; proceeds pay back acquisition debt / cash.
    """
    arv = deal.arv
    purchase = deal.contract_price
    rehab = deal.rehab_cost
    buy_close = deal.contract_price * deal.buy_close_pct

    total_cash_in = purchase + rehab + buy_close

    # Rental NOI
    noi = deal.noi

    # Refi
    refi_loan = arv * refi_ltv
    refi_proceeds = refi_loan - existing_debt
    cash_left_in = max(total_cash_in - refi_proceeds, 0.0)

    r = refi_rate or deal.rate
    monthly_payment = pmt(r, refi_term_years, refi_loan)
    annual_debt_service = monthly_payment * 12

    annual_cash_flow = noi - annual_debt_service
    dscr = noi / annual_debt_service if annual_debt_service > 0 else 0.0
    coc = annual_cash_flow / cash_left_in if cash_left_in > 0 else float("inf")
    equity_created = arv - refi_loan

    flags: list[str] = []
    if refi_proceeds < total_cash_in * 0.75:
        flags.append("LOW_CASH_RECOVERY")
    if dscr < 1.0:
        flags.append("NEGATIVE_DSCR")
    if dscr < 1.25:
        flags.append("DSCR_BELOW_1.25")
    if cash_left_in > total_cash_in * 0.30:
        flags.append("HIGH_CASH_LEFT_IN")
    if noi < 0:
        flags.append("NEGATIVE_NOI")

    return BRRRRResult(
        strategy="BRRRR",
        purchase_price=purchase,
        rehab_cost=rehab,
        buy_closing=buy_close,
        total_cash_in=total_cash_in,
        noi=noi,
        arv=arv,
        refi_ltv=refi_ltv,
        refi_loan=refi_loan,
        refi_proceeds=refi_proceeds,
        cash_left_in=cash_left_in,
        monthly_refi_payment=monthly_payment,
        annual_debt_service=annual_debt_service,
        annual_cash_flow=annual_cash_flow,
        dscr=dscr,
        coc_return=coc,
        equity_created=equity_created,
        viable=dscr >= 1.0 and annual_cash_flow > 0,
        flags=flags,
    )
