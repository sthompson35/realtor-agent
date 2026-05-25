"""
Private_Lending + Note_Buying calculators.
Source: Private_Lending tab, Note_Buying tab — STLLC_Strategy_Arsenal_Calculator.xlsx
"""

from __future__ import annotations
from dataclasses import dataclass
from realtor_agent.calculations._math import irr_monthly, annualize_irr


@dataclass
class PrivateLendingResult:
    strategy: str
    loan_amount: float
    rate: float
    points_pct: float
    term_months: int
    points_income: float
    interest_income: float
    total_return: float
    annualized_yield: float
    ltv: float
    viable: bool
    flags: list[str]


@dataclass
class NoteBuyingResult:
    strategy: str
    note_face_value: float
    purchase_price: float
    discount_pct: float
    monthly_payment: float
    remaining_months: int
    current_yield: float        # annual_payments / purchase_price
    ytm: float                  # yield to maturity (annualized IRR)
    viable: bool
    flags: list[str]


def calc_private_lending(
    loan_amount: float,
    rate: float,
    points_pct: float,
    term_months: int,
    property_value: float = 0.0,
    target_yield: float = 0.10,
) -> PrivateLendingResult:
    """
    Private / hard-money lending analysis from the lender's perspective.

    total_return = interest_income + points_income
    annualized_yield = total_return / (loan_amount × (term_months / 12))
    """
    points_income = loan_amount * points_pct
    interest_income = loan_amount * rate * (term_months / 12)
    total_return = points_income + interest_income
    annualized = total_return / (loan_amount * (term_months / 12)) if term_months > 0 else 0.0
    ltv = loan_amount / property_value if property_value > 0 else 0.0

    flags: list[str] = []
    if ltv > 0.75:
        flags.append("LTV_ABOVE_75PCT")
    if annualized < target_yield:
        flags.append(f"YIELD_BELOW_{int(target_yield*100)}PCT")

    return PrivateLendingResult(
        strategy="Private_Lending",
        loan_amount=loan_amount,
        rate=rate,
        points_pct=points_pct,
        term_months=term_months,
        points_income=points_income,
        interest_income=interest_income,
        total_return=total_return,
        annualized_yield=annualized,
        ltv=ltv,
        viable=ltv <= 0.75 and annualized >= target_yield,
        flags=flags,
    )


def calc_note_buying(
    note_face_value: float,
    purchase_price: float,
    monthly_payment: float,
    remaining_months: int,
    target_yield: float = 0.12,
) -> NoteBuyingResult:
    """
    Note buying — purchase a performing note at a discount.

    current_yield = (monthly_payment × 12) / purchase_price
    YTM = annualized IRR of cash flows (initial outflow + monthly inflows)
    """
    discount_pct = (note_face_value - purchase_price) / note_face_value if note_face_value > 0 else 0.0
    current_yield = (monthly_payment * 12) / purchase_price if purchase_price > 0 else 0.0

    # IRR cash flows: [-purchase] + [monthly_payment × remaining_months]
    cash_flows = [-purchase_price] + [monthly_payment] * remaining_months
    try:
        monthly_irr = irr_monthly(cash_flows)
        ytm = annualize_irr(monthly_irr)
    except Exception:
        ytm = current_yield  # fallback

    flags: list[str] = []
    if discount_pct < 0.10:
        flags.append("LOW_DISCOUNT")
    if ytm < target_yield:
        flags.append(f"YIELD_BELOW_{int(target_yield*100)}PCT")
    if monthly_payment <= 0:
        flags.append("NON_PERFORMING_NOTE")

    return NoteBuyingResult(
        strategy="Note_Buying",
        note_face_value=note_face_value,
        purchase_price=purchase_price,
        discount_pct=discount_pct,
        monthly_payment=monthly_payment,
        remaining_months=remaining_months,
        current_yield=current_yield,
        ytm=ytm,
        viable=ytm >= target_yield and monthly_payment > 0,
        flags=flags,
    )
