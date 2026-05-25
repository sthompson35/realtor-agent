"""
DealIntake — mirrors the Intake sheet (34 columns) in
STLLC_Strategy_Arsenal_Calculator.xlsx.

All fields are optional so callers can supply whatever they have;
strategy calculators validate what they need before computing.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class DealIntake:
    """
    Central deal input model.  Blue-cell values from the Intake sheet.
    Settings sheet defaults are baked in here as Python defaults.
    """

    # --- Identity ---
    deal_id: str = ""
    address: str = ""
    city: str = ""
    state: str = ""
    county: str = ""
    zip_code: str = ""
    asset_type: str = "SFR"         # SFR | MF | Land | Commercial | Duplex | 4plex

    # --- Acquisition ---
    contract_price: float = 0.0     # Purchase / contract price
    arv: float = 0.0                # After-Repair Value
    rehab_cost: float = 0.0         # Total estimated rehab
    dom: int = 0                    # Days on market

    # --- Income ---
    monthly_rent: float = 0.0       # Gross scheduled monthly rent

    # --- Operating Expenses (annual where noted) ---
    taxes: float = 0.0              # Annual property taxes
    insurance: float = 0.0         # Annual insurance
    hoa: float = 0.0                # Monthly HOA (converted to annual internally)
    opex_other: float = 0.0        # Other annual operating expenses

    # --- Expense Ratios (as decimals, e.g. 0.08 = 8%) ---
    vacancy_pct: float = 0.08
    pm_pct: float = 0.08            # Property management
    repairs_pct: float = 0.05       # Maintenance/repairs
    capex_pct: float = 0.05         # Capital expenditure reserve

    # --- Exit / Acquisition Costs ---
    sell_cost_pct: float = 0.08     # Selling costs (commissions + closing)
    buy_close_pct: float = 0.03     # Buying closing costs
    hold_months: int = 6            # Projected hold period

    # --- Financing ---
    rate: float = 0.08              # Annual interest rate (decimal)
    points: float = 0.02            # Loan origination points (decimal)
    down_pct: float = 0.20          # Down payment percentage
    term_years: int = 30            # Loan term in years

    # --- Land-specific ---
    acres: float = 0.0
    zoning: str = ""
    buildable: bool = True          # Kill-switch flag
    road_access: bool = True        # Kill-switch flag
    flood_zone: str = "X"           # AE/VE = high risk; X = safe

    # --- Profit targets (from Settings sheet) ---
    flip_profit_target_pct: float = 0.20
    wholesale_min_fee: float = 5000.0
    investor_margin_pct: float = 0.15   # Investor's profit target for wholesale

    # --- Computed helpers (populated by calculators) ---
    _noi: Optional[float] = field(default=None, repr=False)

    # ------------------------------------------------------------------
    # Derived convenience properties
    # ------------------------------------------------------------------

    @property
    def loan_amount(self) -> float:
        return self.contract_price * (1 - self.down_pct)

    @property
    def down_payment(self) -> float:
        return self.contract_price * self.down_pct

    @property
    def buy_closing_cost(self) -> float:
        return self.contract_price * self.buy_close_pct

    @property
    def annual_hoa(self) -> float:
        return self.hoa * 12

    @property
    def land_kill_switch(self) -> bool:
        """True when the deal should be killed due to land risk flags."""
        return (
            not self.buildable
            or not self.road_access
            or self.flood_zone.upper() in ("AE", "VE")
        )

    @property
    def gross_annual_rent(self) -> float:
        return self.monthly_rent * 12

    @property
    def effective_gross_income(self) -> float:
        return self.gross_annual_rent * (1 - self.vacancy_pct)

    @property
    def annual_operating_expenses(self) -> float:
        ratio_expenses = self.gross_annual_rent * (
            self.pm_pct + self.repairs_pct + self.capex_pct
        )
        fixed_expenses = self.taxes + self.insurance + self.annual_hoa + self.opex_other
        return ratio_expenses + fixed_expenses

    @property
    def noi(self) -> float:
        """Net Operating Income (annual)."""
        return self.effective_gross_income - self.annual_operating_expenses
