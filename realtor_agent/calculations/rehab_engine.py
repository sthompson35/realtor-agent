"""
Rehab Engine — scope pricing, contractor bid comparison, draw schedule.
Source: Rehab_Engine_v2_Contractor_Bid_Compare.xlsx
  06_REHAB_ENGINE_v2    → scope items + pricing
  07_CONTRACTOR_BID_COMPARE → 3-bid comparison
  08_DRAW_SCHEDULE      → construction phases
  REF_SCOPE_PRICING     → unit cost reference table
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


# ---------------------------------------------------------------------------
# Reference Scope Pricing (from REF_SCOPE_PRICING tab)
# ---------------------------------------------------------------------------

class ScopeLevel(str, Enum):
    LIGHT = "light"       # Cosmetic only
    MEDIUM = "medium"     # Systems + cosmetic
    HEAVY = "heavy"       # Structural + full gut

# Unit costs ($/unit or $/sqft as noted).  Reasonable mid-market US averages.
SCOPE_PRICING: dict[str, dict] = {
    # Exterior
    "roof_repair":            {"unit": "sqft", "light": 1.50, "medium": 0,    "heavy": 0},
    "roof_replacement":       {"unit": "sqft", "light": 0,    "medium": 4.50, "heavy": 6.00},
    "exterior_paint":         {"unit": "sqft", "light": 1.50, "medium": 2.00, "heavy": 2.50},
    "siding_replacement":     {"unit": "sqft", "light": 0,    "medium": 0,    "heavy": 9.00},
    "windows_replacement":    {"unit": "unit", "light": 0,    "medium": 400,  "heavy": 600},
    "doors_exterior":         {"unit": "unit", "light": 0,    "medium": 350,  "heavy": 600},
    "driveway_concrete":      {"unit": "sqft", "light": 0,    "medium": 0,    "heavy": 9.00},
    "landscaping_basic":      {"unit": "lump", "light": 1500, "medium": 3000, "heavy": 5000},

    # Interior — Kitchen (mutually exclusive per level)
    "kitchen_cosmetic":       {"unit": "lump", "light": 5000, "medium": 0,     "heavy": 0},
    "kitchen_full_remodel":   {"unit": "lump", "light": 0,    "medium": 15000, "heavy": 30000},
    "appliances_package":     {"unit": "lump", "light": 2500, "medium": 4500,  "heavy": 7000},
    "countertops_granite":    {"unit": "lump", "light": 0,    "medium": 1800,  "heavy": 2700},  # ~30 sqft × $60-90
    "cabinets_reface":        {"unit": "lump", "light": 3000, "medium": 0,     "heavy": 0},
    "cabinets_replace":       {"unit": "lump", "light": 0,    "medium": 8000,  "heavy": 15000},

    # Interior — Bathrooms (mutually exclusive per level)
    "bath_cosmetic":          {"unit": "lump", "light": 2500, "medium": 0,    "heavy": 0},
    "bath_full_remodel":      {"unit": "lump", "light": 0,    "medium": 8000, "heavy": 15000},
    "bath_fixtures":          {"unit": "lump", "light": 1000, "medium": 0,    "heavy": 0},
    "tile_per_bath":          {"unit": "lump", "light": 0,    "medium": 2000, "heavy": 4000},

    # Flooring (choose one finish per level)
    "flooring_lvp":           {"unit": "sqft", "light": 3.50, "medium": 4.50, "heavy": 0},
    "flooring_hardwood":      {"unit": "sqft", "light": 0,    "medium": 0,    "heavy": 10.00},
    "flooring_carpet":        {"unit": "sqft", "light": 2.00, "medium": 0,    "heavy": 0},
    "flooring_tile":          {"unit": "sqft", "light": 0,    "medium": 5.00, "heavy": 8.00},

    # Interior Paint & Finishes
    "interior_paint":         {"unit": "sqft", "light": 1.00, "medium": 1.50, "heavy": 2.00},
    "trim_doors_interior":    {"unit": "unit", "light": 150,  "medium": 200,  "heavy": 300},
    "lighting_fixtures":      {"unit": "lump", "light": 1000, "medium": 2500, "heavy": 5000},

    # Systems — HVAC (service vs replace)
    "hvac_service":           {"unit": "lump", "light": 500,  "medium": 0,     "heavy": 0},
    "hvac_full_replace":      {"unit": "lump", "light": 0,    "medium": 7000,  "heavy": 12000},

    # Systems — Plumbing
    "plumbing_repairs":       {"unit": "lump", "light": 500,  "medium": 2000,  "heavy": 0},
    "plumbing_repiping":      {"unit": "lump", "light": 0,    "medium": 0,     "heavy": 8000},
    "water_heater":           {"unit": "lump", "light": 0,    "medium": 1200,  "heavy": 1800},

    # Systems — Electrical
    "electrical_repairs":     {"unit": "lump", "light": 500,  "medium": 2000,  "heavy": 0},
    "electrical_panel":       {"unit": "lump", "light": 0,    "medium": 3000,  "heavy": 5000},
    "electrical_rewire":      {"unit": "sqft", "light": 0,    "medium": 0,     "heavy": 8.00},

    # Structural (heavy only)
    "demo_haul":              {"unit": "lump", "light": 1000, "medium": 3000,  "heavy": 6000},
    "framing_repairs":        {"unit": "lump", "light": 0,    "medium": 0,     "heavy": 8000},
    "foundation_repair":      {"unit": "lump", "light": 0,    "medium": 0,     "heavy": 15000},
}

# Default draw schedule phases (% of total budget per phase)
DRAW_SCHEDULE_TEMPLATE: list[dict] = [
    {"phase": 1, "label": "Mobilization / Demo",       "pct": 0.10},
    {"phase": 2, "label": "Rough Framing / Foundation","pct": 0.20},
    {"phase": 3, "label": "Rough MEP (HVAC/Plumb/Elec)","pct": 0.20},
    {"phase": 4, "label": "Insulation / Drywall",      "pct": 0.15},
    {"phase": 5, "label": "Finishes / Paint / Flooring","pct": 0.20},
    {"phase": 6, "label": "Punch List / Final",        "pct": 0.15},
]


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class ScopeLineItem:
    name: str
    quantity: float             # sqft, units, or 1 for lump
    unit: str
    unit_cost: float
    total: float


@dataclass
class ContractorBid:
    contractor_name: str
    bid_total: float
    line_items: list[dict] = field(default_factory=list)
    notes: str = ""
    variance_from_low: float = 0.0      # populated by compare()
    variance_pct: float = 0.0


@dataclass
class DrawPhase:
    phase: int
    label: str
    pct: float
    amount: float


@dataclass
class RehabScopeResult:
    scope_level: str
    sqft: float
    num_windows: int
    num_bath: int
    line_items: list[ScopeLineItem]
    subtotal: float
    contingency_pct: float
    contingency_amount: float
    total: float


@dataclass
class BidCompareResult:
    bids: list[ContractorBid]
    low_bid: float
    high_bid: float
    median_bid: float
    spread: float
    recommended_bid: ContractorBid | None


@dataclass
class DrawScheduleResult:
    total_budget: float
    phases: list[DrawPhase]


# ---------------------------------------------------------------------------
# Rehab Scope Calculator
# ---------------------------------------------------------------------------

def calc_rehab_scope(
    scope_level: ScopeLevel | str,
    sqft: float,
    num_windows: int = 10,
    num_bath: int = 2,
    num_doors_interior: int = 8,
    contingency_pct: float = 0.10,
    overrides: Optional[dict[str, float]] = None,
) -> RehabScopeResult:
    """
    Calculate estimated rehab cost from standard scope items.

    Args:
        scope_level: "light" | "medium" | "heavy"
        sqft: Living area square footage.
        num_windows: Number of windows (for window replacement).
        num_bath: Number of full bathrooms.
        num_doors_interior: Interior door count.
        contingency_pct: Contingency buffer (default 10 %).
        overrides: Dict of {scope_item_name: total_cost} to override defaults.
    """
    level = ScopeLevel(scope_level) if isinstance(scope_level, str) else scope_level
    lvl = level.value
    overrides = overrides or {}

    line_items: list[ScopeLineItem] = []

    quantity_map: dict[str, float] = {
        "sqft": sqft,
        "unit": 1,      # overridden per item
        "lump": 1,
    }

    unit_qty_overrides: dict[str, float] = {
        "windows_replacement": num_windows,
        "doors_exterior": 2,
        "doors_exterior": 2,
        "trim_doors_interior": num_doors_interior,
        "bath_full_remodel": num_bath,
        "bath_cosmetic": num_bath,
        "bath_fixtures": num_bath,
        "tile_per_bath": num_bath,
    }

    for item_name, pricing in SCOPE_PRICING.items():
        if item_name in overrides:
            total = overrides[item_name]
            unit_cost = total
        else:
            unit_cost = pricing.get(lvl, 0) or 0
            if unit_cost == 0:
                continue
            qty = unit_qty_overrides.get(item_name, quantity_map.get(pricing["unit"], 1))
            total = unit_cost * qty

        if total == 0:
            continue

        qty = unit_qty_overrides.get(item_name, quantity_map.get(pricing.get("unit", "lump"), 1))
        line_items.append(ScopeLineItem(
            name=item_name,
            quantity=qty,
            unit=pricing.get("unit", "lump"),
            unit_cost=unit_cost,
            total=total,
        ))

    subtotal = sum(li.total for li in line_items)
    contingency_amount = subtotal * contingency_pct
    total = subtotal + contingency_amount

    return RehabScopeResult(
        scope_level=lvl,
        sqft=sqft,
        num_windows=num_windows,
        num_bath=num_bath,
        line_items=line_items,
        subtotal=subtotal,
        contingency_pct=contingency_pct,
        contingency_amount=contingency_amount,
        total=total,
    )


# ---------------------------------------------------------------------------
# Contractor Bid Comparison
# ---------------------------------------------------------------------------

def compare_contractor_bids(bids: list[ContractorBid]) -> BidCompareResult:
    """
    Compare up to 3 contractor bids side-by-side.
    Flags bids that deviate > 20 % from the low bid.
    """
    if not bids:
        return BidCompareResult(bids=[], low_bid=0, high_bid=0, median_bid=0, spread=0, recommended_bid=None)

    sorted_bids = sorted(bids, key=lambda b: b.bid_total)
    low = sorted_bids[0].bid_total
    high = sorted_bids[-1].bid_total
    totals = [b.bid_total for b in bids]
    n = len(totals)
    median = sorted(totals)[n // 2] if n % 2 else (sorted(totals)[n//2-1] + sorted(totals)[n//2]) / 2
    spread = high - low

    for bid in bids:
        bid.variance_from_low = bid.bid_total - low
        bid.variance_pct = (bid.bid_total - low) / low if low > 0 else 0.0

    # Recommend median bid (avoids both low-ball and high-ball)
    recommended = min(bids, key=lambda b: abs(b.bid_total - median))

    return BidCompareResult(
        bids=bids,
        low_bid=low,
        high_bid=high,
        median_bid=median,
        spread=spread,
        recommended_bid=recommended,
    )


# ---------------------------------------------------------------------------
# Draw Schedule
# ---------------------------------------------------------------------------

def calc_draw_schedule(
    total_budget: float,
    custom_phases: Optional[list[dict]] = None,
) -> DrawScheduleResult:
    """
    Generate a construction draw schedule.

    Uses DRAW_SCHEDULE_TEMPLATE unless custom_phases provided.
    custom_phases format: [{"label": str, "pct": float}, ...]
    """
    template = custom_phases or DRAW_SCHEDULE_TEMPLATE
    phases: list[DrawPhase] = []

    for i, phase_def in enumerate(template, start=1):
        pct = phase_def.get("pct", 0)
        phases.append(DrawPhase(
            phase=phase_def.get("phase", i),
            label=phase_def.get("label", f"Phase {i}"),
            pct=pct,
            amount=total_budget * pct,
        ))

    return DrawScheduleResult(total_budget=total_budget, phases=phases)
