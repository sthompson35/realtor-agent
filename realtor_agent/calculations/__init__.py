"""
STLLC Calculation Engine — Phase 1
Pure-Python formula library. No I/O, no DB. Every function is unit-testable.

Ported from:
  STLLC_Strategy_Arsenal_Calculator.xlsx  (24 strategy tabs)
  Rehab_Engine_v2_Contractor_Bid_Compare.xlsx
  closed_deals_archive_companion_v8.xlsx  (portfolio metrics)
  portfolio_rollup_master_v8.xlsx
"""

from realtor_agent.calculations.intake import DealIntake
from realtor_agent.calculations import strategies, rehab_engine, portfolio

__all__ = ["DealIntake", "strategies", "rehab_engine", "portfolio"]
