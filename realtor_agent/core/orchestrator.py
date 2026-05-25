"""
Main orchestrator for the Realtor Agent system.
Coordinates all bots and manages the acquisition workflow.
"""

from typing import Dict, Any, List, Optional
import asyncio
import importlib
import logging
from datetime import datetime
from pathlib import Path

from realtor_agent.core.config import Config
from realtor_agent.utils.logging import LoggerMixin
from realtor_agent.bots.base import BaseBot, BotResult


logger = logging.getLogger(__name__)


class Orchestrator:
    """Lightweight synchronous pipeline orchestrator.

    Dynamically loads any bot that follows the BaseBot contract,
    runs each in sequence, passes a shared context, and collects
    BotResult objects.  A failed bot is recorded and the pipeline
    continues with the remaining bots.

    Usage::

        orchestrator = Orchestrator()
        results = orchestrator.run()
    """

    _DEFAULT_SEQUENCE: List[str] = [
        "web_scout",
        "data_clean",
        "underwriter",
        "deal_desk",
        "owner_finder",
        "outreach",
        "negotiator",
        "compliance_qa",
    ]

    def __init__(
        self,
        bot_names: Optional[List[str]] = None,
        config=None,
    ):
        from realtor_agent.core.config import load_config
        from realtor_agent.core.database import SessionLocal

        self.bot_names = bot_names or self._DEFAULT_SEQUENCE
        self.config = config or load_config()
        self.session = SessionLocal()
        self.context: Dict[str, Any] = {
            "db": self.session,
            "config": self.config,
            "logger": logger,
        }

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def run(self) -> List[BotResult]:
        """Run all bots in sequence and return their results."""
        results: List[BotResult] = []
        for name in self.bot_names:
            result = self._run_one(name)
            results.append(result)
            self.context[name] = result
        self.session.commit()
        return results

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    def _run_one(self, name: str) -> BotResult:
        try:
            bot = self._load_bot(name)
            logger.info("Running bot %s", name)
            result = bot.run(self.context)
            if result.get("status") != "success":
                logger.warning("Bot %s did not succeed – continuing", name)
            return result
        except Exception as exc:
            logger.exception("Bot %s raised an unhandled exception", name)
            return BotResult({"error": str(exc), "bot": name}, status="failed")

    def _load_bot(self, name: str) -> BaseBot:
        """Import and instantiate the bot class for *name*.

        Convention: bot ``foo_bar`` lives in
        ``realtor_agent.bots.foo_bar.foo_bar.FooBarBot``.
        Tries three constructor signatures in order.
        """
        module   = importlib.import_module(f"realtor_agent.bots.{name}.{name}")
        cls_name = name.title().replace("_", "") + "Bot"
        bot_cls  = getattr(module, cls_name)

        for init_args, init_kwargs in [
            ([], {"config": self.config, "database": None}),
            ([], {"logger": logger}),
            ([], {}),
        ]:
            try:
                return bot_cls(*init_args, **init_kwargs)
            except TypeError:
                continue
        raise RuntimeError(f"Cannot instantiate {cls_name} — no matching constructor")


class RealtorOrchestrator(LoggerMixin):
    """
    Main orchestrator that coordinates all real estate acquisition activities.
    """

    def __init__(self, config: Config):
        """
        Initialize the orchestrator.

        Args:
            config: System configuration
        """
        self.config = config
        self.bots: Dict[str, Any] = {}
        self.logger.info("RealtorOrchestrator initialized", config_version=config.version)

    def _get_bot_enabled(self, bot_config: Any) -> Optional[bool]:
        if hasattr(bot_config, "enabled"):
            return bool(bot_config.enabled)
        if isinstance(bot_config, dict) and "enabled" in bot_config:
            return bool(bot_config.get("enabled"))
        return None

    def _set_bot_enabled(self, bot_config: Any, enabled: bool) -> None:
        if hasattr(bot_config, "enabled"):
            bot_config.enabled = enabled
        elif isinstance(bot_config, dict):
            bot_config["enabled"] = enabled

    async def initialize_bots(self) -> None:
        """Initialize all enabled bots."""
        self.logger.info("Initializing bots")

        for bot_name, bot_config in self.config.bots.items():
            enabled = self._get_bot_enabled(bot_config)
            if enabled is None:
                self.logger.info(f"Skipping non-bot config entry: {bot_name}")
                continue
            if not enabled:
                self.logger.info(f"Skipping disabled bot: {bot_name}")
                continue

            try:
                # TODO: Implement actual bot initialization
                self.logger.info(f"Initialized bot: {bot_name}")
                self.bots[bot_name] = {"config": bot_config, "status": "initialized"}

            except Exception as e:
                self.logger.error(f"Failed to initialize bot {bot_name}: {e}")
                raise

        self.logger.info(f"Successfully initialized {len(self.bots)} bots")

    async def run_acquisition_cycle(self) -> None:
        """Run a complete acquisition cycle using the defined playbook."""
        self.logger.info("Starting acquisition cycle with playbook execution")

        try:
            # Playbook Phase 1: SEARCH - Discover listings from permitted sources
            await self._run_search_phase()

            # Playbook Phase 2: UNDERWRITE - Calculate MAO and assess risks
            await self._run_underwrite_phase()

            # Playbook Phase 3: OUTREACH - Contact owners ethically and compliantly
            await self._run_outreach_phase()

            # Playbook Phase 4: NEGOTIATE - Handle counteroffers and concessions
            await self._run_negotiate_phase()

            # Playbook Phase 5: CLOSE - Generate contracts and manage closing pipeline
            await self._run_close_phase()

            self.logger.info("Acquisition cycle completed successfully")

        except Exception as e:
            self.logger.error(f"Acquisition cycle failed: {e}")
            raise

    async def _run_search_phase(self) -> None:
        """Run SEARCH phase: Discover listings from permitted sources."""
        self.logger.info("Running SEARCH phase")

        # Assign Bot 1: Web Scout (Listings Intake)
        if "web_scout" in self.bots:
            await self._execute_bot("web_scout", "search_listings")

        # Assign Bot 2: Data Clean & Enrichment
        if "data_clean" in self.bots:
            await self._execute_bot("data_clean", "clean_and_enrich")

        # Assign Bot 5: Owner Finder (Private Owners)
        if "owner_finder" in self.bots:
            await self._execute_bot("owner_finder", "find_owners")

        # Assign Bot 8: Compliance & QA (ToS, scraping safeguards)
        if "compliance_qa" in self.bots:
            await self._execute_bot("compliance_qa", "check_compliance")

    async def _run_underwrite_phase(self) -> None:
        """Run UNDERWRITE phase: Calculate MAO and assess risks."""
        self.logger.info("Running UNDERWRITE phase")

        # Assign Bot 3: Underwriter (Valuation & MAO)
        if "underwriter" in self.bots:
            await self._execute_bot("underwriter", "calculate_mao")

        # Assign Bot 4: Deal Desk (Docs/Contracts)
        if "deal_desk" in self.bots:
            await self._execute_bot("deal_desk", "prepare_deal_docs")

    async def _run_outreach_phase(self) -> None:
        """Run OUTREACH phase: Contact owners ethically and compliantly."""
        self.logger.info("Running OUTREACH phase")

        # Assign Bot 6: Outreach & Follow Up
        if "outreach_follow" in self.bots:
            await self._execute_bot("outreach_follow", "initiate_outreach")

        # Assign Bot 8: Compliance & QA (Anti-spam, consent, DNC checks)
        if "compliance_qa" in self.bots:
            await self._execute_bot("compliance_qa", "verify_consent")

    async def _run_negotiate_phase(self) -> None:
        """Run NEGOTIATE phase: Handle counteroffers and concessions."""
        self.logger.info("Running NEGOTIATE phase")

        # Assign Bot 7: Negotiator (Counteroffers)
        if "negotiator" in self.bots:
            await self._execute_bot("negotiator", "handle_negotiations")

    async def _run_close_phase(self) -> None:
        """Run CLOSE phase: Generate contracts and manage closing pipeline."""
        self.logger.info("Running CLOSE phase")

        # Assign Bot 4: Deal Desk (Term sheets, contracts)
        if "deal_desk" in self.bots:
            await self._execute_bot("deal_desk", "generate_contracts")

        # Assign Bot 8: Compliance & QA (Document completeness)
        if "compliance_qa" in self.bots:
            await self._execute_bot("compliance_qa", "validate_documents")

    async def _run_market_research(self) -> None:
        """Run market research phase."""
        self.logger.info("Running market research phase")
        await self._run_search_phase()

    async def _run_deal_identification(self) -> None:
        """Run deal identification phase."""
        self.logger.info("Running deal identification phase")
        await self._run_underwrite_phase()

    async def _run_due_diligence(self) -> None:
        """Run due diligence phase."""
        self.logger.info("Running due diligence phase")
        await self._run_outreach_phase()

    async def _run_deal_approval(self) -> None:
        """Run deal approval phase."""
        self.logger.info("Running deal approval phase")
        await self._run_negotiate_phase()

    async def _run_closing_process(self) -> None:
        """Run closing process phase."""
        self.logger.info("Running closing process phase")
        await self._run_close_phase()

    async def _execute_bot(self, bot_name: str, task: str) -> None:
        """Execute a specific task on a bot."""
        self.logger.info(f"Executing task '{task}' on bot '{bot_name}'")

        if bot_name not in self.bots:
            self.logger.warning(f"Bot '{bot_name}' not available for task '{task}'")
            return

        try:
            # TODO: Implement actual bot execution
            # For now, just log the execution
            self.logger.info(f"Task '{task}' completed on bot '{bot_name}'")

        except Exception as e:
            self.logger.error(f"Failed to execute task '{task}' on bot '{bot_name}': {e}")
            raise

    async def get_system_status(self) -> Dict[str, Any]:
        """Get current system status."""
        return {
            "status": "operational",
            "bots_active": len(self.bots),
            "config_version": self.config.version,
            "goals": {
                "target_markets": self.config.goals.target_markets,
                "risk_tolerance": self.config.goals.risk_tolerance,
                "monthly_target": self.config.goals.monthly_deal_target,
            },
        }

    async def shutdown(self) -> None:
        """Shutdown the orchestrator and all bots."""
        self.logger.info("Shutting down orchestrator")

        # TODO: Implement proper bot shutdown
        for bot_name in self.bots.keys():
            self.logger.info(f"Shutting down bot: {bot_name}")

        self.bots.clear()
        self.logger.info("Orchestrator shutdown complete")

    # Synchronous methods for web interface
    def get_deals(self) -> list:
        """Get all deals (synchronous wrapper)."""
        # TODO: Implement real deal retrieval from database
        # For now, return mock data
        return [
            {
                "id": 1,
                "address": "123 Main St, Irvine, CA",
                "price": 750000,
                "status": "Active",
                "bot": "Web Scout",
                "created": "2024-12-10T10:30:00Z",
                "last_updated": "2024-12-10T14:45:00Z",
            },
            {
                "id": 2,
                "address": "456 Oak Ave, Newport Beach, CA",
                "price": 1200000,
                "status": "Under Contract",
                "bot": "Negotiator",
                "created": "2024-12-09T09:15:00Z",
                "last_updated": "2024-12-10T11:20:00Z",
            },
            {
                "id": 3,
                "address": "789 Pine Rd, Mission Viejo, CA",
                "price": 650000,
                "status": "Closed",
                "bot": "Deal Desk",
                "created": "2024-12-08T16:45:00Z",
                "last_updated": "2024-12-09T13:30:00Z",
            },
        ]

    def get_deal(self, deal_id: int) -> Optional[dict]:
        """Get a specific deal by ID."""
        deals = self.get_deals()
        return next((d for d in deals if d["id"] == deal_id), None)

    def get_bot_status(self) -> dict:
        """Get status of all bots."""
        # Return bot status from config and current state
        bot_status = {}
        for bot_name, bot_config in self.config.bots.items():
            enabled = self._get_bot_enabled(bot_config)
            if enabled is None:
                continue
            status = "active" if enabled else "inactive"
            if bot_name in self.bots:
                # Could add more detailed status here
                status = self.bots[bot_name].get("status", status)

            bot_status[bot_name] = {
                "status": status,
                "last_run": None,  # TODO: Track actual last run times
                "enabled": enabled,
            }
        return bot_status

    def toggle_bot(self, bot_name: str) -> dict:
        """Toggle a bot on/off."""
        if bot_name not in self.config.bots:
            return {"error": "Bot not found"}

        enabled = self._get_bot_enabled(self.config.bots[bot_name])
        if enabled is None:
            return {"error": "Bot config missing enabled flag"}

        # Toggle the enabled status in config
        self._set_bot_enabled(self.config.bots[bot_name], not enabled)

        new_enabled = self._get_bot_enabled(self.config.bots[bot_name])
        new_status = "active" if new_enabled else "inactive"

        # TODO: Actually start/stop the bot process

        return {"status": "success", "new_status": new_status, "enabled": new_enabled}

    def get_stats(self) -> dict:
        """Get dashboard statistics."""
        # TODO: Calculate real statistics from database
        return {
            "total_deals": 247,
            "active_deals": 89,
            "closed_deals": 158,
            "avg_ma": 185420,
            "conversion_rate": 23.4,
            "avg_days_to_close": 42,
        }

    def get_recent_activity(self) -> list:
        """Get recent system activity."""
        # TODO: Get real activity from logs/database
        activities = []

        # Add recent deals
        deals = self.get_deals()[:3]
        for deal in deals:
            activities.append(
                {
                    "type": "deal",
                    "icon": "fas fa-plus-circle",
                    "color": "text-success",
                    "message": f"New deal added - {deal['address']}",
                    "timestamp": deal["created"],
                }
            )

        # Add recent bot activities
        bot_activities = [
            {"name": "Web Scout", "action": "completed scan", "icon": "fas fa-robot", "color": "text-primary"},
            {
                "name": "Negotiator",
                "action": "moved deal to under contract",
                "icon": "fas fa-handshake",
                "color": "text-warning",
            },
            {"name": "Data Clean", "action": "processed 15 records", "icon": "fas fa-broom", "color": "text-info"},
        ]

        for activity in bot_activities:
            activities.append(
                {
                    "type": "bot",
                    "icon": activity["icon"],
                    "color": activity["color"],
                    "message": f"{activity['name']} bot {activity['action']}",
                    "timestamp": datetime.now().isoformat(),
                }
            )

        # Sort by timestamp (most recent first)
        activities.sort(key=lambda x: x.get("timestamp", ""), reverse=True)

        return activities[:5]

    def get_system_status(self) -> dict:
        """Get current system status (synchronous wrapper)."""
        # Mock system status - in real implementation, this would check actual services
        bots_data = self.get_bot_status()
        return {
            "database": {"status": "online", "badge": "bg-success", "progress": 100},
            "api": {"status": "operational", "badge": "bg-success", "progress": 100},
            "bots": {
                "status": f"{sum(1 for b in bots_data.values() if b['status'] == 'active')}/{len(bots_data)}",
                "badge": "bg-info",
                "progress": int((sum(1 for b in bots_data.values() if b["status"] == "active") / len(bots_data)) * 100),
            },
        }
