"""Shared financial math primitives used across all strategy calculators."""

from __future__ import annotations


def pmt(annual_rate: float, term_years: int, principal: float) -> float:
    """
    Monthly loan payment (Excel PMT equivalent).

    Args:
        annual_rate: Annual interest rate as decimal (e.g. 0.08 for 8%).
        term_years: Loan term in years.
        principal: Loan principal.

    Returns:
        Monthly payment amount (positive = outflow).
    """
    if principal <= 0:
        return 0.0
    r = annual_rate / 12
    n = term_years * 12
    if r == 0:
        return principal / n
    return principal * r / (1 - (1 + r) ** -n)


def irr_monthly(cash_flows: list[float], guess: float = 0.01) -> float:
    """
    Internal Rate of Return (monthly) via Newton-Raphson.
    cash_flows[0] is the initial investment (negative).
    Returns monthly IRR; multiply by 12 for approximate annual IRR.
    """
    rate = guess
    for _ in range(1000):
        npv = sum(cf / (1 + rate) ** i for i, cf in enumerate(cash_flows))
        d_npv = sum(-i * cf / (1 + rate) ** (i + 1) for i, cf in enumerate(cash_flows))
        if d_npv == 0:
            break
        new_rate = rate - npv / d_npv
        if abs(new_rate - rate) < 1e-8:
            rate = new_rate
            break
        rate = new_rate
    return rate


def annualize_irr(monthly_irr: float) -> float:
    return (1 + monthly_irr) ** 12 - 1
