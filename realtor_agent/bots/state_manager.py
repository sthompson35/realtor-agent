import json
import pickle
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, Optional
from ..core.logger import get_logger
from ..core.config import config

logger = get_logger(__name__)


class BotStateManager:
    """Manage bot state persistence"""

    def __init__(self, state_dir: str = None):
        self.state_dir = Path(state_dir or "data/bot_states")
        self.state_dir.mkdir(parents=True, exist_ok=True)

    def save_state(self, bot_name: str, state: Dict[str, Any]):
        """Save bot state to disk"""
        try:
            state_file = self.state_dir / f"{bot_name}_state.json"
            state_data = {"bot_name": bot_name, "timestamp": datetime.utcnow().isoformat(), "state": state}

            with open(state_file, "w") as f:
                json.dump(state_data, f, indent=2)

            logger.info(f"Saved state for bot: {bot_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to save state for {bot_name}: {e}")
            return False

    def load_state(self, bot_name: str) -> Optional[Dict[str, Any]]:
        """Load bot state from disk"""
        try:
            state_file = self.state_dir / f"{bot_name}_state.json"

            if not state_file.exists():
                logger.info(f"No saved state found for bot: {bot_name}")
                return None

            with open(state_file, "r") as f:
                state_data = json.load(f)

            logger.info(f"Loaded state for bot: {bot_name}")
            return state_data.get("state")
        except Exception as e:
            logger.error(f"Failed to load state for {bot_name}: {e}")
            return None

    def clear_state(self, bot_name: str):
        """Clear bot state"""
        try:
            state_file = self.state_dir / f"{bot_name}_state.json"
            if state_file.exists():
                state_file.unlink()
                logger.info(f"Cleared state for bot: {bot_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to clear state for {bot_name}: {e}")
            return False

    def list_states(self) -> list:
        """List all saved bot states"""
        try:
            states = []
            for state_file in self.state_dir.glob("*_state.json"):
                bot_name = state_file.stem.replace("_state", "")
                states.append(
                    {
                        "bot_name": bot_name,
                        "file": str(state_file),
                        "modified": datetime.fromtimestamp(state_file.stat().st_mtime).isoformat(),
                    }
                )
            return states
        except Exception as e:
            logger.error(f"Failed to list bot states: {e}")
            return []


# Global state manager instance
bot_state_manager = BotStateManager()
