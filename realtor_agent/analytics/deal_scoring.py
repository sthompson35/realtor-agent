from typing import Dict, Any, Optional
from datetime import datetime
from ..core.logger import get_logger

logger = get_logger(__name__)


class DealScorer:
    """Calculate deal scores based on multiple factors"""

    def __init__(self):
        self.strategy_weights = {
            "buy_and_hold": {"yield": 0.40, "stability": 0.25, "appreciation": 0.20, "risk_penalty": -0.15},
            "fix_and_flip": {"discount": 0.50, "renovation_potential": 0.25, "velocity": 0.20, "risk_penalty": -0.15},
            "owner_occupant": {"affordability": 0.35, "stability": 0.25, "qol": 0.25, "liquidity": 0.15},
        }

    def calculate_deal_score(self, property_data: Dict[str, Any], strategy: str) -> float:
        """Calculate overall deal score for a property"""
        if strategy not in self.strategy_weights:
            logger.warning(f"Unknown strategy: {strategy}")
            return 0.0

        if strategy == "buy_and_hold":
            return self._score_buy_and_hold(property_data)
        elif strategy == "fix_and_flip":
            return self._score_fix_and_flip(property_data)
        elif strategy == "owner_occupant":
            return self._score_owner_occupant(property_data)

        return 0.0

    def _score_buy_and_hold(self, data: Dict[str, Any]) -> float:
        """Score for buy and hold strategy"""
        weights = self.strategy_weights["buy_and_hold"]

        # Calculate yield score (rental income / purchase price)
        price = data.get("price", 0)
        monthly_rent = data.get("estimated_rent", 0)
        annual_rent = monthly_rent * 12
        yield_score = (annual_rent / price * 100) if price > 0 else 0
        yield_score = min(yield_score / 10, 1.0)

        # Calculate stability score
        days_on_market = data.get("days_on_market", 0)
        stability_score = max(0, 1 - (days_on_market / 180))

        # Calculate appreciation potential
        market_trend = data.get("market_trend", 0)
        appreciation_score = (market_trend + 10) / 20

        # Calculate risk penalty
        risk_flags = len(data.get("risk_flags", []))
        risk_penalty = min(risk_flags * 0.1, 0.5)

        # Weighted score
        score = (
            yield_score * weights["yield"]
            + stability_score * weights["stability"]
            + appreciation_score * weights["appreciation"]
            - risk_penalty * abs(weights["risk_penalty"])
        )

        return max(0, min(score, 1.0))

    def _score_fix_and_flip(self, data: Dict[str, Any]) -> float:
        """Score for fix and flip strategy"""
        weights = self.strategy_weights["fix_and_flip"]

        # Calculate discount score
        list_price = data.get("price", 0)
        arv = data.get("arv_estimate", list_price)
        renovation_cost = data.get("estimated_renovation_cost", 0)

        potential_profit = arv - list_price - renovation_cost
        discount_score = (potential_profit / arv) if arv > 0 else 0
        discount_score = max(0, min(discount_score * 2, 1.0))

        # Calculate renovation potential
        condition = data.get("condition_est", "good")
        renovation_potential = {"excellent": 0.2, "good": 0.4, "fair": 0.7, "poor": 1.0}.get(condition, 0.5)

        # Calculate velocity score (how fast it will sell)
        days_on_market = data.get("days_on_market", 0)
        avg_dom = data.get("market_avg_days_on_market", 30)
        velocity_score = max(0, 1 - (days_on_market / (avg_dom * 2)))

        # Calculate risk penalty
        risk_flags = len(data.get("risk_flags", []))
        risk_penalty = min(risk_flags * 0.1, 0.5)

        # Weighted score
        score = (
            discount_score * weights["discount"]
            + renovation_potential * weights["renovation_potential"]
            + velocity_score * weights["velocity"]
            - risk_penalty * abs(weights["risk_penalty"])
        )

        return max(0, min(score, 1.0))

    def _score_owner_occupant(self, data: Dict[str, Any]) -> float:
        """Score for owner occupant strategy"""
        weights = self.strategy_weights["owner_occupant"]

        # Calculate affordability score
        price = data.get("price", 0)
        median_income = data.get("market_median_income", 60000)
        affordable_price = median_income * 3
        affordability_score = max(0, 1 - (price / affordable_price - 1))

        # Calculate stability score
        year_built = data.get("year_built", 2000)
        current_year = datetime.now().year
        age = current_year - year_built
        stability_score = max(0, 1 - (age / 100))

        # Calculate quality of life score
        school_rating = data.get("school_rating", 5) / 10
        crime_score = 1 - (data.get("crime_index", 50) / 100)
        qol_score = (school_rating + crime_score) / 2

        # Calculate liquidity score
        days_on_market = data.get("days_on_market", 0)
        liquidity_score = max(0, 1 - (days_on_market / 90))

        # Weighted score
        score = (
            affordability_score * weights["affordability"]
            + stability_score * weights["stability"]
            + qol_score * weights["qol"]
            + liquidity_score * weights["liquidity"]
        )

        return max(0, min(score, 1.0))

    def calculate_combined_score(self, property_data: Dict[str, Any]) -> Dict[str, float]:
        """Calculate scores for all strategies"""
        return {
            "buy_and_hold": self.calculate_deal_score(property_data, "buy_and_hold"),
            "fix_and_flip": self.calculate_deal_score(property_data, "fix_and_flip"),
            "owner_occupant": self.calculate_deal_score(property_data, "owner_occupant"),
        }


# Global deal scorer instance
deal_scorer = DealScorer()
