"""
Case study seed data from the STLLC Training Workbook.
Pre-loads 5 real properties used across all 12 training lessons.

Usage:
    from realtor_agent.core.seed_data import seed_case_studies
    seed_case_studies()   # idempotent — skips existing deal_ids
"""

from __future__ import annotations
from datetime import datetime
import uuid

CASE_STUDIES = [
    # ─────────────────────────────────────────────────────────
    # CS1 — Clean Fix & Flip  (Lesson 1, 2, 3, 10, 11)
    # ─────────────────────────────────────────────────────────
    {
        "deal_id":          "CS1-ELM-DESLOGE",
        "address":          "412 Elm Street",
        "city":             "Desloge",
        "state":            "MO",
        "county":           "St. Francois",
        "zip_code":         "63601",
        "asset_type":       "SFR",
        "contract_price":   85000.0,
        "arv":              155000.0,
        "rehab_cost":       28000.0,
        "monthly_rent":     1100.0,
        "taxes":            1200.0,
        "insurance":        900.0,
        "hoa":              0.0,
        "hold_months":      5,
        "rate":             0.08,
        "down_pct":         0.20,
        "term_years":       30,
        "sell_cost_pct":    0.08,
        "buy_close_pct":    0.03,
        "vacancy_pct":      0.08,
        "pm_pct":           0.08,
        "repairs_pct":      0.05,
        "capex_pct":        0.05,
        "flip_profit_target_pct": 0.20,
        "wholesale_min_fee":      5000.0,
        "status":           "qualified",
        "priority":         "high",
        "source":           "Training Workbook CS1",
        "notes":            "Training Case Study 1 — Clean Fix & Flip. 1350 sqft, 3BR/2BA. "
                            "Expected ROI ~21.3% → BUY signal.",
        "score":            85.0,
        "deal_score":       88.0,
    },

    # ─────────────────────────────────────────────────────────
    # CS2 — BRRRR Duplex  (Lesson 4, 5, 9, 11)
    # ─────────────────────────────────────────────────────────
    {
        "deal_id":          "CS2-LEADBELT-PARKHILLS",
        "address":          "789 Lead Belt Drive",
        "city":             "Park Hills",
        "state":            "MO",
        "county":           "St. Francois",
        "zip_code":         "63601",
        "asset_type":       "Duplex",
        "contract_price":   62000.0,
        "arv":              140000.0,
        "rehab_cost":       65000.0,
        "monthly_rent":     1800.0,   # combined both units
        "taxes":            1500.0,
        "insurance":        1400.0,
        "hoa":              0.0,
        "hold_months":      8,
        "rate":             0.08,
        "down_pct":         0.25,
        "term_years":       30,
        "sell_cost_pct":    0.08,
        "buy_close_pct":    0.03,
        "vacancy_pct":      0.08,
        "pm_pct":           0.08,
        "repairs_pct":      0.05,
        "capex_pct":        0.05,
        "flip_profit_target_pct": 0.20,
        "wholesale_min_fee":      5000.0,
        "status":           "qualified",
        "priority":         "high",
        "source":           "Training Workbook CS2",
        "notes":            "Training Case Study 2 — BRRRR Duplex. 2100 sqft, both units rented. "
                            "75% refi LTV target. Heavy rehab → BRRRR strategy.",
        "score":            78.0,
        "deal_score":       82.0,
    },

    # ─────────────────────────────────────────────────────────
    # CS3 — Wholesale Assignment  (Lesson 7, 11)
    # ─────────────────────────────────────────────────────────
    {
        "deal_id":          "CS3-SILVERCREEK-BONNETERRE",
        "address":          "156 Silver Creek Lane",
        "city":             "Bonne Terre",
        "state":            "MO",
        "county":           "St. Francois",
        "zip_code":         "63628",
        "asset_type":       "SFR",
        "contract_price":   35000.0,
        "arv":              105000.0,
        "rehab_cost":       38000.0,
        "monthly_rent":     800.0,
        "taxes":            900.0,
        "insurance":        750.0,
        "hoa":              0.0,
        "hold_months":      3,
        "rate":             0.08,
        "down_pct":         0.20,
        "term_years":       30,
        "sell_cost_pct":    0.08,
        "buy_close_pct":    0.03,
        "vacancy_pct":      0.08,
        "pm_pct":           0.08,
        "repairs_pct":      0.05,
        "capex_pct":        0.05,
        "flip_profit_target_pct": 0.20,
        "wholesale_min_fee":      5000.0,
        "status":           "lead",
        "priority":         "medium",
        "source":           "Training Workbook CS3",
        "notes":            "Training Case Study 3 — Wholesale. Seller bottom $30K, back taxes $2,400. "
                            "950 sqft. MAO at 70% rule = $35,500. Assignment fee target.",
        "score":            65.0,
        "deal_score":       70.0,
    },

    # ─────────────────────────────────────────────────────────
    # CS4 — JV Partnership Victorian  (Lesson 5, 6, 11)
    # ─────────────────────────────────────────────────────────
    {
        "deal_id":          "CS4-COLUMBIA-FARMINGTON",
        "address":          "220 W Columbia Street",
        "city":             "Farmington",
        "state":            "MO",
        "county":           "St. Francois",
        "zip_code":         "63640",
        "asset_type":       "SFR",
        "contract_price":   125000.0,
        "arv":              285000.0,
        "rehab_cost":       95000.0,
        "monthly_rent":     2200.0,
        "taxes":            2400.0,
        "insurance":        2000.0,
        "hoa":              0.0,
        "hold_months":      10,
        "rate":             0.08,
        "down_pct":         0.30,   # 70/30 capital split
        "term_years":       30,
        "sell_cost_pct":    0.08,
        "buy_close_pct":    0.03,
        "vacancy_pct":      0.08,
        "pm_pct":           0.08,
        "repairs_pct":      0.05,
        "capex_pct":        0.05,
        "flip_profit_target_pct": 0.20,
        "wholesale_min_fee":      5000.0,
        "status":           "under_contract",
        "priority":         "high",
        "source":           "Training Workbook CS4",
        "notes":            "Training Case Study 4 — JV Partnership. 3200 sqft Victorian. "
                            "70/30 capital split, 50/50 profit split after management fee.",
        "score":            90.0,
        "deal_score":       92.0,
    },

    # ─────────────────────────────────────────────────────────
    # CS5 — Multi-Strategy Cape Cod  (Lesson 10, 11, 12)
    # ─────────────────────────────────────────────────────────
    {
        "deal_id":          "CS5-OAKHILL-PARKHILLS",
        "address":          "534 Oak Hill Road",
        "city":             "Park Hills",
        "state":            "MO",
        "county":           "St. Francois",
        "zip_code":         "63601",
        "asset_type":       "SFR",
        "contract_price":   78000.0,
        "arv":              168000.0,
        "rehab_cost":       35000.0,
        "monthly_rent":     1300.0,
        "taxes":            1600.0,
        "insurance":        1100.0,
        "hoa":              0.0,
        "hold_months":      6,
        "rate":             0.08,
        "down_pct":         0.20,
        "term_years":       30,
        "sell_cost_pct":    0.08,
        "buy_close_pct":    0.03,
        "vacancy_pct":      0.08,
        "pm_pct":           0.08,
        "repairs_pct":      0.05,
        "capex_pct":        0.05,
        "flip_profit_target_pct": 0.20,
        "wholesale_min_fee":      5000.0,
        "status":           "lead",
        "priority":         "medium",
        "source":           "Training Workbook CS5",
        "notes":            "Training Case Study 5 — Multi-strategy comparison. 1550 sqft Cape Cod. "
                            "5 comps range $158K–$175.5K. 75% refi LTV target. Compare all exit strategies.",
        "score":            80.0,
        "deal_score":       84.0,
    },
]


def seed_case_studies(run_underwriter: bool = True) -> dict:
    """
    Insert the 5 training case studies into the DB. Idempotent — skips existing deal_ids.
    Optionally runs underwriter bot to populate underwriting_results.
    Returns {"inserted": int, "skipped": int, "errors": list}.
    """
    from realtor_agent.core.models import SessionLocal, DealIntakeModel
    from realtor_agent.bots.underwriter.underwriter import UnderwriterBot

    db = SessionLocal()
    inserted = 0
    skipped  = 0
    errors   = []

    try:
        for cs in CASE_STUDIES:
            existing = db.query(DealIntakeModel).filter_by(deal_id=cs["deal_id"]).first()
            if existing:
                skipped += 1
                continue
            try:
                row = DealIntakeModel(**cs)
                db.add(row)
                db.commit()
                db.refresh(row)
                inserted += 1

                if run_underwriter:
                    # Underwrite asynchronously (no-op if bot import fails)
                    try:
                        bot = UnderwriterBot()
                        bot.run({"web_scout": {"listings": [cs]}})
                    except Exception as uw_exc:
                        errors.append(f"Underwriter for {cs['deal_id']}: {uw_exc}")

            except Exception as exc:
                db.rollback()
                errors.append(f"{cs['deal_id']}: {exc}")
    finally:
        db.close()

    return {"inserted": inserted, "skipped": skipped, "errors": errors}
