"""Strategy calculator modules — one per STLLC strategy tab."""

from realtor_agent.calculations.strategies.flip import (
    calc_fix_and_flip,
    calc_wholetail,
    FlipResult,
)
from realtor_agent.calculations.strategies.wholesale import (
    calc_wholesale_assignment,
    calc_novation,
    WholesaleResult,
    NovationResult,
)
from realtor_agent.calculations.strategies.brrrr import calc_brrrr, BRRRRResult
from realtor_agent.calculations.strategies.rental import (
    calc_rental_buy_hold,
    calc_small_multifamily,
    RentalResult,
    MultifamilyResult,
)
from realtor_agent.calculations.strategies.creative_finance import (
    calc_subject_to,
    calc_seller_finance,
    calc_wrap,
    SubToResult,
    SellerFinanceResult,
    WrapResult,
)
from realtor_agent.calculations.strategies.land import (
    calc_land_wholesale,
    calc_land_flip_cash,
    calc_land_flip_terms,
    LandWholesaleResult,
    LandFlipCashResult,
    LandFlipTermsResult,
)
from realtor_agent.calculations.strategies.lending import (
    calc_private_lending,
    calc_note_buying,
    PrivateLendingResult,
    NoteBuyingResult,
)
from realtor_agent.calculations.strategies.option import (
    calc_option_control,
    calc_subdivision_split,
    OptionResult,
    SubdivisionResult,
)
from realtor_agent.calculations.strategies.analysis import (
    calc_sensitivity_analysis,
    calc_stress_test,
    calc_jv_partnership,
    calc_exit_decision,
    calc_dispo,
    calc_tax_estimate,
    SensitivityResult,
    StressTestResult,
    JVResult,
    ExitDecisionResult,
    DispoResult,
    TaxEstimateResult,
)

__all__ = [
    "calc_fix_and_flip", "calc_wholetail", "FlipResult",
    "calc_wholesale_assignment", "calc_novation", "WholesaleResult", "NovationResult",
    "calc_brrrr", "BRRRRResult",
    "calc_rental_buy_hold", "calc_small_multifamily", "RentalResult", "MultifamilyResult",
    "calc_subject_to", "calc_seller_finance", "calc_wrap",
    "SubToResult", "SellerFinanceResult", "WrapResult",
    "calc_land_wholesale", "calc_land_flip_cash", "calc_land_flip_terms",
    "LandWholesaleResult", "LandFlipCashResult", "LandFlipTermsResult",
    "calc_private_lending", "calc_note_buying", "PrivateLendingResult", "NoteBuyingResult",
    "calc_option_control", "calc_subdivision_split", "OptionResult", "SubdivisionResult",
    "calc_sensitivity_analysis", "calc_stress_test", "calc_jv_partnership",
    "calc_exit_decision", "calc_dispo", "calc_tax_estimate",
    "SensitivityResult", "StressTestResult", "JVResult",
    "ExitDecisionResult", "DispoResult", "TaxEstimateResult",
]
