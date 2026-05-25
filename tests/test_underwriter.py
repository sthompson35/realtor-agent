"""
Underwriter bot tests.

Covers:
  - BotResult contract
  - calc_mao_flip / calc_mao_rental pure helpers
  - UnderwriterBot.run() via the BaseBot interface
  - Legacy YAML-config tests (kept for regression)
"""

import pytest
import yaml
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from realtor_agent.bots.base import BaseBot, BotResult
from realtor_agent.bots.underwriter.underwriter import (
    UnderwriterBot,
    calc_mao_flip,
    calc_mao_rental,
)


# ---------------------------------------------------------------------------
# BotResult contract
# ---------------------------------------------------------------------------

class TestBotResult:
    def test_default_status_is_success(self):
        result = BotResult({"mao": 50_000})
        assert result["status"] == "success"

    def test_explicit_status(self):
        result = BotResult({"error": "no comps"}, status="failed")
        assert result["status"] == "failed"

    def test_empty_data(self):
        result = BotResult()
        assert result["status"] == "success"
        assert len(result) == 1  # only the 'status' key

    def test_is_dict_subclass(self):
        result = BotResult({"x": 1, "y": 2})
        assert isinstance(result, dict)
        assert result["x"] == 1


# ---------------------------------------------------------------------------
# BaseBot contract
# ---------------------------------------------------------------------------

class TestBaseBotContract:
    def test_underwriter_is_basebot(self):
        assert issubclass(UnderwriterBot, BaseBot)

    def test_underwriter_has_name(self):
        assert UnderwriterBot.name == "underwriter"

    def test_abstract_run_enforced(self):
        """A class that skips run() cannot be instantiated."""
        with pytest.raises(TypeError):
            class Broken(BaseBot):
                name = "broken"
            Broken()


# ---------------------------------------------------------------------------
# calc_mao_flip
# ---------------------------------------------------------------------------

class TestCalcMaoFlip:
    def test_basic_flip(self):
        # ARV=200k, rehab=30k, 3-month hold
        mao = calc_mao_flip(arv=200_000, rehab=30_000)
        assert mao > 0
        assert mao < 200_000

    def test_formula_values(self):
        arv, rehab = 100_000, 10_000
        expected = (
            arv
            - rehab
            - arv * 0.01 * 3   # holding (default 3 months @ 1%)
            - arv * 0.08        # selling  (default 8%)
            - arv * 0.20        # profit   (default 20%)
        )
        assert calc_mao_flip(arv=arv, rehab=rehab) == pytest.approx(expected)

    def test_negative_when_upside_down(self):
        # Rehab exceeds all remaining value → negative MAO
        mao = calc_mao_flip(arv=50_000, rehab=80_000)
        assert mao < 0

    def test_custom_params(self):
        mao_standard = calc_mao_flip(arv=200_000, rehab=20_000)
        mao_longer_hold = calc_mao_flip(arv=200_000, rehab=20_000, hold_months=12)
        assert mao_longer_hold < mao_standard  # longer hold = lower MAO


# ---------------------------------------------------------------------------
# calc_mao_rental
# ---------------------------------------------------------------------------

class TestCalcMaoRental:
    def test_basic_rental(self):
        mao = calc_mao_rental(monthly_rent=1_500, rehab=20_000)
        assert mao > 0

    def test_arv_ceiling_applied(self):
        # With a low ARV ceiling the cap limits the MAO
        mao_capped = calc_mao_rental(
            monthly_rent=1_500, rehab=5_000, arv_ceiling=100_000
        )
        assert mao_capped <= 100_000 * 0.75

    def test_no_ceiling(self):
        mao = calc_mao_rental(monthly_rent=2_000, rehab=10_000)
        # NOI=24k / 0.08 cap = 300k value; 300k - 10k rehab = 290k
        assert mao == pytest.approx(290_000)

    def test_higher_cap_rate_lowers_mao(self):
        mao_8 = calc_mao_rental(monthly_rent=1_500, rehab=10_000, cap_rate_target=0.08)
        mao_10 = calc_mao_rental(monthly_rent=1_500, rehab=10_000, cap_rate_target=0.10)
        assert mao_8 > mao_10


# ---------------------------------------------------------------------------
# UnderwriterBot.run() via BaseBot interface
# ---------------------------------------------------------------------------

class TestUnderwriterBotRun:
    def _make_bot(self):
        return UnderwriterBot()

    def test_run_empty_context_returns_success(self):
        bot = self._make_bot()
        result = bot.run({})
        assert result["status"] == "success"
        assert result["total_count"] == 0
        assert result["approved_count"] == 0

    def test_run_with_listings(self):
        bot = self._make_bot()
        context = {
            "web_scout": {
                "listings": [
                    {"property_id": "p1", "address": "123 Main St", "sqft": 1200, "price": 90_000},
                    {"property_id": "p2", "address": "456 Oak Ave", "sqft": 800,  "price": 55_000},
                ]
            }
        }
        result = bot.run(context)
        assert result["status"] == "success"
        assert result["total_count"] == 2
        assert isinstance(result["results"], list)
        for r in result["results"]:
            assert "mao" in r
            assert "roi" in r
            assert "approved" in r
            assert isinstance(r["approved"], bool)

    def test_run_returns_bot_result_instance(self):
        bot = self._make_bot()
        result = bot.run({})
        assert isinstance(result, BotResult)

    def test_run_approved_count_consistent(self):
        bot = self._make_bot()
        context = {
            "web_scout": {
                "listings": [
                    {"property_id": "p1", "sqft": 2000},
                    {"property_id": "p2", "sqft": 100},  # tiny sqft → low ARV → likely rejected
                ]
            }
        }
        result = bot.run(context)
        approved = [r for r in result["results"] if r["approved"]]
        assert result["approved_count"] == len(approved)


# ---------------------------------------------------------------------------
# Legacy YAML-config tests (regression)
# ---------------------------------------------------------------------------

class MockUnderwriterBot:
    def __init__(self, config_path, knowledge_path):
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)
        with open(knowledge_path, "r") as f:
            self.knowledge = yaml.safe_load(f)

    def calculate_mao_flip(self, arv, rehab_cost, purchase_price):
        profit_margin = self.config["formulas"]["flip"]["profit_margin"]
        holding_months = self.config["costs"]["holding"]["months"]
        holding_cost = (
            purchase_price
            * self.config["costs"]["holding"]["monthly_percent"]
            * holding_months
        )
        closing_cost = purchase_price * self.config["costs"]["closing"]["percent"]
        mao = (arv * (1 - profit_margin)) - rehab_cost - holding_cost - closing_cost
        return max(0, mao)

    def assess_risks(self, property_data):
        risk_flags = []
        if property_data.get("flood_zone") == "high":
            risk_flags.append("floodway_wetlands")
        if not property_data.get("utilities_access", True):
            risk_flags.append("no_utilities")
        if property_data.get("title_issues", False):
            risk_flags.append("clouded_title")
        return risk_flags


@pytest.fixture(scope="module")
def mock_bot():
    return MockUnderwriterBot(
        "bots/underwriter/bot_config.yml",
        "realtor_agent_knowledge_pack.yml",
    )


def test_underwriter_config(mock_bot):
    assert mock_bot.config["enabled"] is True
    assert "valuation" in mock_bot.config
    assert "rehab" in mock_bot.config
    assert "formulas" in mock_bot.config


def test_mao_calculation(mock_bot):
    mao = mock_bot.calculate_mao_flip(arv=100_000, rehab_cost=15_000, purchase_price=60_000)
    assert mao > 0
    assert mao < 60_000


def test_risk_assessment(mock_bot):
    property_data = {"flood_zone": "high", "utilities_access": False, "title_issues": True}
    risks = mock_bot.assess_risks(property_data)
    assert isinstance(risks, list)
    assert len(risks) > 0
    assert "floodway_wetlands" in risks
    assert "no_utilities" in risks
    assert "clouded_title" in risks


def test_underwriter_knowledge_integration(mock_bot):
    assert "core_formulas" in mock_bot.knowledge
    assert "mao_flip" in mock_bot.knowledge["core_formulas"]
