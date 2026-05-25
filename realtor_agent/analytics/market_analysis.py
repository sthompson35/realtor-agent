from typing import Dict, List, Any
from datetime import datetime, timedelta
import json
from pathlib import Path
from ..core.logger import get_logger

logger = get_logger(__name__)


class MarketTrendAnalyzer:
    """Analyze market trends and patterns"""

    def __init__(self, data_dir: str = "realtor_agent"):
        self.data_dir = Path(data_dir)

    def load_market_data(self) -> Dict[str, Any]:
        """Load market data from reports"""
        try:
            markets_file = self.data_dir / "US_BEST_MARKETS_REPORT.json"
            deals_file = self.data_dir / "US_BEST_DEALS_REPORT.json"

            markets_data = {}
            deals_data = {}

            if markets_file.exists():
                with open(markets_file, "r") as f:
                    markets_data = json.load(f)

            if deals_file.exists():
                with open(deals_file, "r") as f:
                    deals_data = json.load(f)

            return {"markets": markets_data, "deals": deals_data}
        except Exception as e:
            logger.error(f"Failed to load market data: {e}")
            return {}

    def analyze_price_trends(self, market_id: str = None) -> Dict[str, Any]:
        """Analyze price trends for markets"""
        data = self.load_market_data()

        if not data.get("markets"):
            return {}

        strategies = data["markets"].get("strategies", {})

        trends = {}
        for strategy_name, strategy_data in strategies.items():
            markets = strategy_data.get("top_markets", [])

            if market_id:
                markets = [m for m in markets if m.get("geo_id") == market_id]

            if not markets:
                continue

            prices = [m.get("core_metrics", {}).get("median_list_price", 0) for m in markets]
            avg_price = sum(prices) / len(prices) if prices else 0

            trends[strategy_name] = {
                "avg_price": round(avg_price, 2),
                "min_price": min(prices) if prices else 0,
                "max_price": max(prices) if prices else 0,
                "market_count": len(markets),
            }

        return trends

    def analyze_inventory_trends(self) -> Dict[str, Any]:
        """Analyze inventory levels across markets"""
        data = self.load_market_data()

        if not data.get("markets"):
            return {}

        strategies = data["markets"].get("strategies", {})

        inventory_analysis = {}
        for strategy_name, strategy_data in strategies.items():
            markets = strategy_data.get("top_markets", [])

            inventory_counts = [m.get("core_metrics", {}).get("inventory_count", 0) for m in markets]

            if not inventory_counts:
                continue

            inventory_analysis[strategy_name] = {
                "avg_inventory": round(sum(inventory_counts) / len(inventory_counts), 1),
                "total_inventory": sum(inventory_counts),
                "low_inventory_markets": len([i for i in inventory_counts if i < 50]),
                "high_inventory_markets": len([i for i in inventory_counts if i > 200]),
            }

        return inventory_analysis

    def analyze_velocity_trends(self) -> Dict[str, Any]:
        """Analyze days on market trends"""
        data = self.load_market_data()

        if not data.get("markets"):
            return {}

        strategies = data["markets"].get("strategies", {})

        velocity_analysis = {}
        for strategy_name, strategy_data in strategies.items():
            markets = strategy_data.get("top_markets", [])

            dom_values = [m.get("core_metrics", {}).get("avg_days_on_market", 0) for m in markets]

            if not dom_values:
                continue

            velocity_analysis[strategy_name] = {
                "avg_days_on_market": round(sum(dom_values) / len(dom_values), 1),
                "fast_markets": len([d for d in dom_values if d < 30]),
                "slow_markets": len([d for d in dom_values if d > 60]),
                "market_tempo": (
                    "fast"
                    if sum(dom_values) / len(dom_values) < 30
                    else "moderate" if sum(dom_values) / len(dom_values) < 60 else "slow"
                ),
            }

        return velocity_analysis

    def get_top_markets_by_strategy(self, strategy: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get top performing markets for a strategy"""
        data = self.load_market_data()

        if not data.get("markets"):
            return []

        strategies = data["markets"].get("strategies", {})
        strategy_data = strategies.get(strategy, {})
        markets = strategy_data.get("top_markets", [])

        return markets[:limit]

    def analyze_deal_opportunities(self, strategy: str = None) -> Dict[str, Any]:
        """Analyze deal opportunities"""
        data = self.load_market_data()

        if not data.get("deals"):
            return {}

        strategies = data["deals"].get("strategies", {})

        if strategy and strategy in strategies:
            strategy_data = strategies[strategy]
            deals = strategy_data.get("top_deals", [])

            return {
                "strategy": strategy,
                "total_deals": len(deals),
                "avg_score": (
                    round(
                        sum(d.get("strategy_alignment", {}).get(f"deal_score_{strategy}", 0) for d in deals)
                        / len(deals),
                        2,
                    )
                    if deals
                    else 0
                ),
                "deals": deals[:10],
            }

        # Analyze all strategies
        analysis = {}
        for strategy_name, strategy_data in strategies.items():
            deals = strategy_data.get("top_deals", [])

            analysis[strategy_name] = {
                "total_deals": len(deals),
                "avg_score": (
                    round(
                        sum(d.get("strategy_alignment", {}).get(f"deal_score_{strategy_name}", 0) for d in deals)
                        / len(deals),
                        2,
                    )
                    if deals
                    else 0
                ),
            }

        return analysis

    def get_market_summary(self) -> Dict[str, Any]:
        """Get comprehensive market summary"""
        return {
            "price_trends": self.analyze_price_trends(),
            "inventory_trends": self.analyze_inventory_trends(),
            "velocity_trends": self.analyze_velocity_trends(),
            "deal_opportunities": self.analyze_deal_opportunities(),
        }


# Global market trend analyzer instance
market_trend_analyzer = MarketTrendAnalyzer()
