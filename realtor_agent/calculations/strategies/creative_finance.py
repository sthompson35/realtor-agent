"""
Subject-To, Seller Finance, and Wrap calculators.
Source: SubTo tab, Seller_Finance tab, Wrap tab — STLLC_Strategy_Arsenal_Calculator.xlsx
"""

from __future__ import annotations
from dataclasses import dataclass
from realtor_agent.calculations.intake import DealIntake
from realtor_agent.calculations._math import pmt


@dataclass
class SubToResult:
    strategy: str
    existing_loan_balance: float
    existing_monthly_payment: float
    seller_equity: float            # purchase_price - existing_loan_balance
    cash_needed: float              # seller equity + closing
    monthly_rent: float
    monthly_pm: float
    monthly_repairs: float
    monthly_spread: float           # rent - existing_payment - pm - repairs
    annual_cash_flow: float
    coc_return: float
    viable: bool
    flags: list[str]


@dataclass
class SellerFinanceResult:
    strategy: str
    purchase_price: float
    down_payment: float
    loan_amount: float
    rate: float
    term_years: int
    monthly_payment: float
    annual_debt_service: float
    noi: float
    dscr: float
    annual_cash_flow: float
    coc_return: float
    equity_in: float
    viable: bool
    flags: list[str]


@dataclass
class WrapResult:
    strategy: str
    wrap_balance: float
    wrap_rate: float
    wrap_payment: float             # payment buyer makes to us
    underlying_balance: float
    underlying_payment: float       # payment we make to original lender
    monthly_spread: float           # our income
    annual_spread: float
    viable: bool
    flags: list[str]


def calc_subject_to(
    deal: DealIntake,
    existing_loan_balance: float = 0.0,
    existing_monthly_payment: float = 0.0,
) -> SubToResult:
    """
    Subject-To — we take title subject to existing financing.

    Cash needed = seller equity (purchase price - loan balance) + closing costs.
    Monthly spread = rent - existing_payment - PM - repairs.
    """
    seller_equity = deal.contract_price - existing_loan_balance
    cash_needed = seller_equity + deal.buy_closing_cost

    pm = deal.monthly_rent * deal.pm_pct
    repairs = deal.monthly_rent * deal.repairs_pct
    monthly_spread = deal.monthly_rent - existing_monthly_payment - pm - repairs

    annual_cf = monthly_spread * 12
    equity_in = max(cash_needed, 1.0)
    coc = annual_cf / equity_in

    flags: list[str] = []
    if monthly_spread < 0:
        flags.append("NEGATIVE_MONTHLY_SPREAD")
    if existing_loan_balance > deal.contract_price * 0.90:
        flags.append("HIGH_LTV_EXISTING")
    if seller_equity < 0:
        flags.append("SELLER_UNDERWATER")

    return SubToResult(
        strategy="Subject_To",
        existing_loan_balance=existing_loan_balance,
        existing_monthly_payment=existing_monthly_payment,
        seller_equity=seller_equity,
        cash_needed=cash_needed,
        monthly_rent=deal.monthly_rent,
        monthly_pm=pm,
        monthly_repairs=repairs,
        monthly_spread=monthly_spread,
        annual_cash_flow=annual_cf,
        coc_return=coc,
        viable=monthly_spread > 0,
        flags=flags,
    )


def calc_seller_finance(deal: DealIntake) -> SellerFinanceResult:
    """
    Seller Carry-Back / Seller Finance note math.

    We (buyer) pay the seller a note. DSCR is from our rental NOI vs the note payment.
    """
    loan = deal.loan_amount
    down = deal.down_payment
    monthly_pmt = pmt(deal.rate, deal.term_years, loan)
    ads = monthly_pmt * 12
    noi = deal.noi

    dscr = noi / ads if ads > 0 else 0.0
    acf = noi - ads
    equity_in = down + deal.buy_closing_cost + deal.rehab_cost
    coc = acf / equity_in if equity_in > 0 else 0.0

    flags: list[str] = []
    if dscr < 1.0:
        flags.append("NEGATIVE_DSCR")
    if dscr < 1.25:
        flags.append("DSCR_BELOW_1.25")
    if deal.rate > 0.10:
        flags.append("HIGH_RATE")

    return SellerFinanceResult(
        strategy="Seller_Finance",
        purchase_price=deal.contract_price,
        down_payment=down,
        loan_amount=loan,
        rate=deal.rate,
        term_years=deal.term_years,
        monthly_payment=monthly_pmt,
        annual_debt_service=ads,
        noi=noi,
        dscr=dscr,
        annual_cash_flow=acf,
        coc_return=coc,
        equity_in=equity_in,
        viable=dscr >= 1.25,
        flags=flags,
    )


def calc_wrap(
    deal: DealIntake,
    wrap_balance: float = 0.0,
    wrap_rate: float = 0.0,
    wrap_term_years: int = 30,
    underlying_balance: float = 0.0,
    underlying_payment: float = 0.0,
) -> WrapResult:
    """
    Wraparound mortgage — we originate a new note to the buyer that wraps
    around the existing underlying note we continue to pay.

    Our monthly income = wrap_payment - underlying_payment.
    """
    if wrap_balance == 0:
        wrap_balance = deal.arv * 0.80
    if wrap_rate == 0:
        wrap_rate = deal.rate + 0.02  # typical spread over underlying

    wrap_pmt = pmt(wrap_rate, wrap_term_years, wrap_balance)
    monthly_spread = wrap_pmt - underlying_payment
    annual_spread = monthly_spread * 12

    flags: list[str] = []
    if monthly_spread <= 0:
        flags.append("NEGATIVE_SPREAD")
    if wrap_balance < underlying_balance:
        flags.append("WRAP_BELOW_UNDERLYING")

    return WrapResult(
        strategy="Wrap",
        wrap_balance=wrap_balance,
        wrap_rate=wrap_rate,
        wrap_payment=wrap_pmt,
        underlying_balance=underlying_balance,
        underlying_payment=underlying_payment,
        monthly_spread=monthly_spread,
        annual_spread=annual_spread,
        viable=monthly_spread > 0,
        flags=flags,
    )
