"""
Base contract for all pipeline bots.

Every bot must:
  1. Inherit from BaseBot
  2. Set a unique ``name`` class attribute
  3. Implement ``run(context) -> BotResult``

The ``context`` dict is populated by the Orchestrator before each call:
  * ``db``       – active SQLAlchemy session
  * ``config``   – application Config object
  * ``logger``   – shared stdlib logger
  * ``<name>``   – BotResult from any previously-run bot (e.g. ``context["web_scout"]``)
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class BotResult(dict):
    """Thin dict wrapper that carries a ``status`` flag alongside result data.

    ``status`` is ``'success'`` (default) or ``'failed'``.

    Example::

        result = BotResult({"mao": 55000, "roi": 0.22})
        assert result["status"] == "success"
        assert result["mao"] == 55000
    """

    def __init__(
        self,
        data: Optional[Dict[str, Any]] = None,
        *,
        status: str = "success",
    ):
        super().__init__(data or {})
        self["status"] = status


class BaseBot(ABC):
    """Abstract base class that every pipeline bot must subclass.

    Subclasses keep their own ``__init__`` signatures; the only requirement
    is implementing ``run(context)``.
    """

    name: str = "base"

    @abstractmethod
    def run(self, context: dict) -> BotResult:
        """Execute the bot's primary work and return a BotResult.

        Args:
            context: Shared pipeline context dict (see module docstring).

        Returns:
            BotResult with ``status='success'`` or ``status='failed'``.
        """
        ...
