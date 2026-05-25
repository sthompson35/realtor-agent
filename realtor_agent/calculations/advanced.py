"""
Advanced calculation engines from the STLLC Training Workbook.

Covers:
  1. Sensitivity Analysis   — 7×7 grid (purchase ±15% vs ARV ±15%)
  2. Stress Test            — Best / Base / Worst scenarios
  3. JV Partnership         — preferred-return waterfall
  4. Exit Strategy Compare  — Flip, Wholesale, Hold, BRRRR side-by-side
  5. Wholesale MAO          — 70% / 65% rule + buyer-profit analysis
  6. Tax Estimator          — Federal 24%, MO 5%, SE 15.3%
  7. Draw Schedule          — 6-phase construction disbursement
  8. Comp Analysis          — up to 5 comps with adjustments
  9. Pipeline Metrics       — probability-weighted values
 10. Property Comparison    — composite ranking matrix

All functions are pure (no DB access) and return plain dicts.
"""

from __future__ import annotations
import math


# ============================================================
# 1. SENSITIVITY ANALYSIS  (7×7 grid)
# ============================================================

def calc_sensitivity_grid(
    base_purchase: float,
    arv: float,
    rehab: float,
    hold_months: int = 6,
    sell_cost_pct: float = 0.08,
    buy_close_pct: float = 0.03,
    hold_cost_monthly_pct: float = 0.01,   # % of ARV per month
    steps: int = 7,
    pct_range: float = 0.15,
) -> dict:
    """
    7×7 matrix varying purchase price ±15% vs ARV ±15% in 5-pct steps.
    Each cell shows net_profit, ROI, and BUY/HOLD/PASS signal.
    """
    half = steps // 2
    offsets = [round(-pct_range + i * (pct_range / half), 4) for i in range(steps)]

    matrix = []
    for arv_off in offsets:
        adj_arv = arv * (1 + arv_off)
        row = []
        for price_off in offsets:
            adj_price = base_purchase * (1 + price_off)
            selling   = adj_arv * sell_cost_pct
            holding   = adj_arv * hold_cost_monthly_pct * hold_months
            buy_close = adj_price * buy_close_pct
            total_in  = adj_price + rehab + selling + holding + buy_close
            net_profit = adj_arv - total_in
            roi = net_profit / total_in if total_in > 0 else 0.0
            row.append({
                "arv_adj_pct":   round(arv_off * 100, 1),
                "price_adj_pct": round(price_off * 100, 1),
                "adj_arv":       round(adj_arv, 2),
                "adj_price":     round(adj_price, 2),
                "net_profit":    round(net_profit, 2),
                "roi_pct":       round(roi * 100, 2),
                "signal":        "BUY" if roi >= 0.20 else ("HOLD" if roi >= 0.10 else "PASS"),
            })
        matrix.append(row)

    return {
        "base_purchase":     base_purchase,
        "base_arv":          arv,
        "rehab":             rehab,
        "hold_months":       hold_months,
        "price_offsets_pct": [round(o * 100, 1) for o in offsets],
        "arv_offsets_pct":   [round(o * 100, 1) for o in offsets],
        "matrix":            matrix,
        "cells_total":       steps * steps,
        "cells_viable":      sum(1 for row in matrix for c in row if c["signal"] != "PASS"),
    }


# ============================================================
# 2. STRESS TEST  (Best / Base / Worst)
# ============================================================

_STRESS_CONFIGS = {
    "best":  {"arv_m": 1.10, "rehab_m": 0.90, "rent_m": 1.05, "hold_m": 0.90, "vac_m": 0.50},
    "base":  {"arv_m": 1.00, "rehab_m": 1.00, "rent_m": 1.00, "hold_m": 1.00, "vac_m": 1.00},
    "worst": {"arv_m": 0.90, "rehab_m": 1.20, "rent_m": 0.95, "hold_m": 1.20, "vac_m": 1.50},
}


def calc_stress_scenarios(
    purchase: float,
    arv: float,
    rehab: float,
    monthly_rent: float,
    hold_months: int = 6,
    sell_cost_pct: float = 0.08,
    buy_close_pct: float = 0.03,
    hold_cost_monthly: float = 0.0,   # absolute $; 0 = 1% of adj ARV/month
    vacancy_pct: float = 0.08,
) -> dict:
    """
    Best / Base / Worst scenarios with standard multipliers.
    Includes break-even months (rent to recover total investment).
    """
    results = {}
    for name, m in _STRESS_CONFIGS.items():
        adj_arv    = arv  * m["arv_m"]
        adj_rehab  = rehab * m["rehab_m"]
        adj_rent   = monthly_rent * m["rent_m"]
        adj_vac    = vacancy_pct  * m["vac_m"]
        hold_unit  = (hold_cost_monthly or adj_arv * 0.01) * m["hold_m"]

        selling    = adj_arv * sell_cost_pct
        total_hold = hold_unit * hold_months
        buy_close  = purchase  * buy_close_pct
        total_in   = purchase + adj_rehab + selling + total_hold + buy_close
        net_profit = adj_arv - total_in
        roi        = net_profit / total_in if total_in > 0 else 0.0

        eff_rent    = adj_rent * (1 - adj_vac)
        be_months   = round(total_in / eff_rent, 1) if eff_rent > 0 else None

        results[name] = {
            "adj_arv":            round(adj_arv, 2),
            "adj_rehab":          round(adj_rehab, 2),
            "adj_rent":           round(adj_rent, 2),
            "hold_cost_monthly":  round(hold_unit, 2),
            "total_in":           round(total_in, 2),
            "net_profit":         round(net_profit, 2),
            "roi_pct":            round(roi * 100, 2),
            "break_even_months":  be_months,
            "signal":             "BUY" if roi >= 0.20 else ("HOLD" if roi >= 0.10 else "PASS"),
        }

    return {
        "purchase":  purchase,
        "base_arv":  arv,
        "base_rehab": rehab,
        "scenarios": results,
        "viable_scenarios": sum(1 for v in results.values() if v["signal"] != "PASS"),
    }


# ============================================================
# 3. JV PARTNERSHIP WATERFALL
# ============================================================

def calc_jv_waterfall(
    total_profit: float,
    partners: list[dict],
    total_capital: float,
    management_fee_pct: float = 0.02,
) -> dict:
    """
    JV waterfall: management fee first → preferred returns → split remaining.

    partners list: [
      {"name": str, "capital": float, "preferred_return_pct": float, "profit_split_pct": float}
    ]
    """
    mgmt_fee  = total_capital * management_fee_pct
    remaining = total_profit - mgmt_fee

    # Preferred returns (pro-rata to available remaining)
    preferred_paid: dict[str, float] = {}
    for p in partners:
        pref = p["capital"] * p.get("preferred_return_pct", 0.08)
        paid = min(pref, max(0.0, remaining))
        preferred_paid[p["name"]] = paid
        remaining -= paid

    # Remaining profit splits
    partner_results = []
    for p in partners:
        split    = max(0.0, remaining) * p.get("profit_split_pct", 0.50)
        total_ret = preferred_paid.get(p["name"], 0.0) + split
        roi_pct  = total_ret / p["capital"] * 100 if p["capital"] > 0 else 0.0
        partner_results.append({
            "name":              p["name"],
            "capital":           p["capital"],
            "capital_pct":       round(p["capital"] / total_capital * 100, 1) if total_capital > 0 else 0.0,
            "preferred_return":  round(preferred_paid.get(p["name"], 0.0), 2),
            "split_profit":      round(split, 2),
            "total_return":      round(total_ret, 2),
            "roi_pct":           round(roi_pct, 2),
        })

    return {
        "total_profit":           total_profit,
        "total_capital":          total_capital,
        "management_fee":         round(mgmt_fee, 2),
        "preferred_returns_paid": round(sum(preferred_paid.values()), 2),
        "remaining_for_split":    round(max(0.0, remaining), 2),
        "partners":               partner_results,
    }


# ============================================================
# 4. EXIT STRATEGY COMPARISON
# ============================================================

def calc_exit_comparison(
    purchase: float,
    arv: float,
    rehab: float,
    monthly_rent: float,
    hold_months: int = 6,
    sell_cost_pct: float = 0.08,
    buy_close_pct: float = 0.03,
    rate: float = 0.08,
    down_pct: float = 0.20,
    term_years: int = 30,
    vacancy_pct: float = 0.08,
    pm_pct: float = 0.08,
    repairs_pct: float = 0.05,
    capex_pct: float = 0.05,
    taxes: float = 0.0,
    insurance: float = 0.0,
    hoa: float = 0.0,
    refi_ltv: float = 0.75,
    wholesale_fee: float = 5000.0,
) -> dict:
    """Compare Fix & Flip, Wholesale, Rental Hold, and BRRRR side by side."""
    from realtor_agent.calculations._math import pmt

    buy_close = purchase * buy_close_pct

    # ── Fix & Flip ─────────────────────────────────────────────
    holding_flip      = arv * 0.01 * hold_months
    selling           = arv * sell_cost_pct
    loan_flip         = purchase * (1 - down_pct)
    monthly_pmt_flip  = pmt(rate, term_years, loan_flip)
    interest_flip     = monthly_pmt_flip * hold_months
    total_in_flip     = purchase + rehab + holding_flip + selling + buy_close + interest_flip
    flip_profit       = arv - total_in_flip
    flip_roi          = flip_profit / total_in_flip if total_in_flip > 0 else 0.0

    # ── Wholesale ──────────────────────────────────────────────
    ws_mao     = arv * 0.70 - rehab - wholesale_fee
    ws_profit  = ws_mao - purchase if ws_mao > purchase else 0.0
    ws_total   = purchase + buy_close
    ws_roi     = ws_profit / ws_total if ws_total > 0 else 0.0
    ws_viable  = ws_mao >= purchase

    # ── Rental Hold ────────────────────────────────────────────
    gross_rent = monthly_rent * 12
    eff_income = gross_rent * (1 - vacancy_pct)
    op_exp     = gross_rent * (pm_pct + repairs_pct + capex_pct) + taxes + insurance + hoa * 12
    noi        = eff_income - op_exp
    loan_hold  = purchase * (1 - down_pct)
    ann_debt   = pmt(rate, term_years, loan_hold) * 12
    cash_flow  = noi - ann_debt
    cash_invest = purchase * down_pct + rehab + buy_close
    coc        = cash_flow / cash_invest if cash_invest > 0 else 0.0
    cap_rate   = noi / purchase if purchase > 0 else 0.0
    dscr       = noi / ann_debt if ann_debt > 0 else 0.0

    # ── BRRRR ──────────────────────────────────────────────────
    refi_amount    = arv * refi_ltv
    total_in_brrrr = purchase + rehab + buy_close
    cash_left_in   = max(0.0, total_in_brrrr - refi_amount)
    brrrr_coc      = cash_flow / cash_left_in if cash_left_in > 0 else 999.0
    equity_capture = arv - purchase - rehab

    def _sig(r: float) -> str:
        return "BUY" if r >= 0.20 else ("HOLD" if r >= 0.10 else "PASS")

    strategies = [
        ("Fix_and_Flip",  flip_roi,   flip_profit > 0),
        ("Wholesale",     ws_roi,     ws_viable),
        ("Rental_Hold",   coc,        dscr >= 1.0 and coc > 0),
        ("BRRRR",         brrrr_coc,  cash_left_in < purchase * 0.30),
    ]
    best = max([(n, r) for n, r, v in strategies if v], key=lambda x: x[1], default=("None", 0))

    return {
        "inputs": {
            "purchase": purchase, "arv": arv, "rehab": rehab,
            "monthly_rent": monthly_rent, "hold_months": hold_months,
        },
        "Fix_and_Flip": {
            "total_in": round(total_in_flip, 2), "net_profit": round(flip_profit, 2),
            "roi_pct": round(flip_roi * 100, 2), "signal": _sig(flip_roi), "viable": flip_profit > 0,
        },
        "Wholesale": {
            "mao": round(ws_mao, 2), "assignment_fee": round(ws_profit, 2),
            "roi_pct": round(ws_roi * 100, 2), "signal": "GO" if ws_viable else "NO-GO", "viable": ws_viable,
        },
        "Rental_Hold": {
            "noi": round(noi, 2), "annual_cash_flow": round(cash_flow, 2),
            "coc_return_pct": round(coc * 100, 2), "cap_rate_pct": round(cap_rate * 100, 2),
            "dscr": round(dscr, 3), "signal": _sig(coc), "viable": dscr >= 1.0 and coc > 0,
        },
        "BRRRR": {
            "refi_amount": round(refi_amount, 2), "cash_left_in": round(cash_left_in, 2),
            "equity_capture": round(equity_capture, 2),
            "coc_return_pct": round(min(brrrr_coc, 9.99) * 100, 2),
            "signal": _sig(coc), "viable": cash_left_in < purchase * 0.30,
        },
        "recommended": best[0],
    }


# ============================================================
# 5. WHOLESALE MAO CALCULATOR
# ============================================================

def calc_wholesale_mao(
    arv: float,
    rehab: float,
    buyer_target_profit_pct: float = 0.20,
    assignment_fee: float = 5000.0,
) -> dict:
    """
    70% rule, 65% rule, and buyer-profit analysis.
    Returns GO / CAUTION / NO-GO viability flag.
    """
    mao_70     = arv * 0.70 - rehab
    mao_65     = arv * 0.65 - rehab
    buyer_profit = arv * buyer_target_profit_pct
    mao_buyer  = arv - rehab - buyer_profit - assignment_fee
    rec_mao    = min(mao_70, mao_buyer)

    viability = (
        "GO"       if rec_mao > 0 and rec_mao >= arv * 0.50
        else "CAUTION" if rec_mao > 0
        else "NO-GO"
    )

    return {
        "arv":                 arv,
        "rehab":               rehab,
        "assignment_fee":      assignment_fee,
        "mao_70_rule":         round(mao_70, 2),
        "mao_65_rule":         round(mao_65, 2),
        "buyer_profit":        round(buyer_profit, 2),
        "mao_buyer_analysis":  round(mao_buyer, 2),
        "recommended_mao":     round(rec_mao, 2),
        "equity_spread_70":    round(arv - mao_70 - rehab, 2),
        "equity_spread_buyer": round(arv - mao_buyer - rehab, 2),
        "viability":           viability,
    }


# ============================================================
# 6. TAX ESTIMATOR
# ============================================================

def calc_taxes(
    net_profit: float,
    strategy: str = "flip",
    purchase_price: float = 0.0,
    hold_years: float = 1.0,
    land_value_pct: float = 0.20,
    federal_rate: float = 0.24,
    state_rate: float = 0.05,
    se_tax_rate: float = 0.153,
) -> dict:
    """
    Tax estimate for flip or hold.
    Flips: Federal 24% + MO 5% + SE 15.3%.
    Holds: Federal 24% + MO 5%, less annual depreciation shelter.
    Depreciation: (purchase × building_pct) ÷ 27.5 per year.
    """
    is_flip = strategy.lower() in ("flip", "fix_and_flip", "wholesale", "wholetail")

    building_value    = purchase_price * (1 - land_value_pct)
    annual_depreciation = building_value / 27.5
    depreciation_benefit = annual_depreciation * hold_years if not is_flip else 0.0

    taxable_income = net_profit - depreciation_benefit
    federal_tax    = taxable_income * federal_rate
    state_tax      = taxable_income * state_rate
    se_tax         = net_profit    * se_tax_rate if is_flip else 0.0

    total_tax      = federal_tax + state_tax + se_tax
    after_tax      = net_profit  - total_tax
    eff_rate       = total_tax   / net_profit if net_profit > 0 else 0.0

    return {
        "net_profit":            round(net_profit, 2),
        "strategy":              strategy,
        "is_flip":               is_flip,
        "annual_depreciation":   round(annual_depreciation, 2),
        "depreciation_benefit":  round(depreciation_benefit, 2),
        "taxable_income":        round(taxable_income, 2),
        "federal_tax":           round(federal_tax, 2),
        "state_tax":             round(state_tax, 2),
        "se_tax":                round(se_tax, 2),
        "total_tax":             round(total_tax, 2),
        "after_tax_profit":      round(after_tax, 2),
        "effective_rate_pct":    round(eff_rate * 100, 2),
        "rates_used": {
            "federal": federal_rate,
            "state":   state_rate,
            "se_tax":  se_tax_rate if is_flip else 0.0,
        },
    }


# ============================================================
# 7. CONSTRUCTION DRAW SCHEDULE
# ============================================================

_DEFAULT_DRAW_PHASES = [
    {"phase": "Pre-Construction",  "pct": 0.10, "description": "Permits, plans, mobilization"},
    {"phase": "Demo & Rough-In",   "pct": 0.25, "description": "Demolition, framing, rough plumbing/electrical"},
    {"phase": "MEP",               "pct": 0.25, "description": "Mechanical, Electrical, Plumbing finals"},
    {"phase": "Interior Finishes", "pct": 0.20, "description": "Drywall, flooring, cabinetry, fixtures"},
    {"phase": "Exterior",          "pct": 0.15, "description": "Siding, roofing, landscaping, exterior paint"},
    {"phase": "Punch List",        "pct": 0.05, "description": "Final inspection, touch-ups, certificate of occupancy"},
]


def calc_draw_schedule(
    total_rehab: float,
    contingency_pct: float = 0.10,
    phases: list[dict] | None = None,
) -> dict:
    """
    6-phase draw schedule with running totals.
    Contingency is listed separately (not distributed per phase).
    """
    contingency  = total_rehab * contingency_pct
    total_w_cont = total_rehab + contingency
    phase_list   = phases or _DEFAULT_DRAW_PHASES

    draws = []
    cumulative = 0.0
    for ph in phase_list:
        amount      = total_rehab * ph["pct"]
        cumulative += amount
        draws.append({
            "phase":          ph["phase"],
            "description":    ph.get("description", ""),
            "pct":            ph["pct"],
            "amount":         round(amount, 2),
            "cumulative":     round(cumulative, 2),
            "cumulative_pct": round(cumulative / total_rehab * 100, 1) if total_rehab > 0 else 0.0,
        })

    return {
        "total_rehab":             total_rehab,
        "contingency_pct":         contingency_pct,
        "contingency":             round(contingency, 2),
        "total_with_contingency":  round(total_w_cont, 2),
        "phases":                  draws,
        "phase_count":             len(draws),
    }


# ============================================================
# 8. COMPARABLE SALES ANALYSIS
# ============================================================

def calc_comp_analysis(
    subject: dict,
    comps: list[dict],
    price_per_sqft_adj: float = 20.0,
    bed_adj: float = 3000.0,
    bath_adj: float = 2000.0,
    age_adj: float = 500.0,
    condition_adj: float = 5000.0,
) -> dict:
    """
    Up to 5-comp analysis with adjustments for sqft, beds, baths, age, condition.
    Total adjustments are capped at ±15% of each comp's sale price.

    subject / comp dict keys:
      sqft, beds, baths, age (years old), condition_score (1=poor … 5=excellent),
      sale_price (comps only), address (comps only)
    """
    adjusted = []
    for comp in comps[:5]:
        raw = comp.get("sale_price", 0)
        if raw <= 0:
            continue

        sqft_diff = subject.get("sqft", 0) - comp.get("sqft", 0)
        bed_diff  = subject.get("beds", 0) - comp.get("beds", 0)
        bath_diff = subject.get("baths", 0) - comp.get("baths", 0)
        age_diff  = comp.get("age", 0)  - subject.get("age", 0)
        cond_diff = subject.get("condition_score", 3) - comp.get("condition_score", 3)

        sq_adj   = (sqft_diff / 100) * price_per_sqft_adj
        bd_adj   = bed_diff  * bed_adj
        ba_adj   = bath_diff * bath_adj
        ag_adj   = (age_diff / 5) * age_adj
        co_adj   = cond_diff * condition_adj

        raw_adj  = sq_adj + bd_adj + ba_adj + ag_adj + co_adj
        max_adj  = raw * 0.15
        capped   = max(-max_adj, min(max_adj, raw_adj))
        adj_pct  = raw_adj / raw * 100

        adjusted.append({
            "address":        comp.get("address", ""),
            "sale_price":     raw,
            "sqft_adj":       round(sq_adj, 2),
            "bed_adj":        round(bd_adj, 2),
            "bath_adj":       round(ba_adj, 2),
            "age_adj":        round(ag_adj, 2),
            "condition_adj":  round(co_adj, 2),
            "raw_adjustment": round(raw_adj, 2),
            "adj_pct":        round(adj_pct, 1),
            "capped":         abs(raw_adj) > max_adj,
            "adjusted_price": round(raw + capped, 2),
        })

    if not adjusted:
        return {"error": "No valid comps provided"}

    adj_prices = [c["adjusted_price"] for c in adjusted]
    sorted_prices = sorted(adj_prices)

    return {
        "subject":         subject,
        "comps":           adjusted,
        "comp_count":      len(adjusted),
        "low_adjusted":    round(min(adj_prices), 2),
        "high_adjusted":   round(max(adj_prices), 2),
        "median_adjusted": round(sorted_prices[len(sorted_prices) // 2], 2),
        "reconciled_arv":  round(sum(adj_prices) / len(adj_prices), 2),
        "price_per_sqft":  round(
            (sum(adj_prices) / len(adj_prices)) / subject.get("sqft", 1), 2
        ) if subject.get("sqft") else None,
    }


# ============================================================
# 9. PIPELINE METRICS  (probability-weighted value)
# ============================================================

STAGE_PROBABILITIES: dict[str, float] = {
    "lead":           0.10,
    "prospect":       0.25,
    "qualified":      0.25,
    "offer_sent":     0.50,
    "under_contract": 0.50,
    "due_diligence":  0.75,
    "closing":        0.90,
    "closed":         1.00,
    "dead":           0.00,
}


def calc_pipeline_metrics(stages: dict) -> dict:
    """
    stages = {stage_name: {"count": int, "total_value": float}}
    Returns weighted pipeline value and per-stage breakdown.
    """
    weighted_value = 0.0
    total_value    = 0.0
    total_count    = 0
    breakdown      = []

    for stage, data in stages.items():
        prob    = STAGE_PROBABILITIES.get(stage, 0.10)
        val     = float(data.get("total_value", 0))
        cnt     = int(data.get("count", 0))
        weighted = val * prob
        weighted_value += weighted
        total_value    += val
        total_count    += cnt
        breakdown.append({
            "stage":           stage,
            "count":           cnt,
            "total_value":     round(val, 2),
            "probability_pct": round(prob * 100),
            "weighted_value":  round(weighted, 2),
        })

    breakdown.sort(key=lambda x: STAGE_PROBABILITIES.get(x["stage"], 0), reverse=True)

    return {
        "total_deals":            total_count,
        "total_pipeline_value":   round(total_value, 2),
        "weighted_pipeline_value": round(weighted_value, 2),
        "stages":                 breakdown,
    }


# ============================================================
# 10. PROPERTY COMPARISON MATRIX
# ============================================================

def calc_property_comparison(properties: list[dict]) -> dict:
    """
    Multi-property composite ranking.

    Each property dict: {
      name/address, price, roi_pct, cash_flow,
      equity_capture, cap_rate_pct
    }
    Weights: ROI 35%, Cash Flow 25%, Equity Capture 20%, Cap Rate 20%.
    """
    if not properties:
        return {"error": "No properties provided", "properties": []}

    METRICS  = ["roi_pct", "cash_flow", "equity_capture", "cap_rate_pct"]
    WEIGHTS  = {"roi_pct": 0.35, "cash_flow": 0.25, "equity_capture": 0.20, "cap_rate_pct": 0.20}

    mins = {m: min(p.get(m, 0.0) for p in properties) for m in METRICS}
    maxs = {m: max(p.get(m, 0.0) for p in properties) for m in METRICS}

    ranked = []
    for p in properties:
        scores    = {}
        composite = 0.0
        for m in METRICS:
            lo, hi = mins[m], maxs[m]
            raw    = p.get(m, 0.0)
            norm   = (raw - lo) / (hi - lo) * 100 if hi > lo else 50.0
            scores[m] = round(norm, 1)
            composite += norm * WEIGHTS[m]

        ranked.append({
            "name":           p.get("name") or p.get("address", ""),
            "price":          p.get("price", 0),
            "roi_pct":        p.get("roi_pct", 0),
            "cash_flow":      p.get("cash_flow", 0),
            "equity_capture": p.get("equity_capture", 0),
            "cap_rate_pct":   p.get("cap_rate_pct", 0),
            "scores":         scores,
            "composite_score": round(composite, 1),
            "signal":         "BUY" if p.get("roi_pct", 0) >= 20 else ("HOLD" if p.get("roi_pct", 0) >= 10 else "PASS"),
        })

    ranked.sort(key=lambda x: x["composite_score"], reverse=True)
    for i, r in enumerate(ranked):
        r["rank"] = i + 1

    return {
        "property_count": len(ranked),
        "top_pick":       ranked[0]["name"] if ranked else None,
        "properties":     ranked,
        "weights_used":   WEIGHTS,
    }
