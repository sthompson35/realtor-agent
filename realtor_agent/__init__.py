"""
Realtor Agent - AI-Powered Real Estate Acquisition System
© Shylow Thompson. LLC 2026 - All Rights Reserved

This package provides an intelligent real estate agent system with:
- Automated lead generation and qualification
- Deal analysis and scoring
- Market trend analysis
- CRM integration
- Workflow automation
- Multi-channel notifications
"""

__version__ = "1.0.0"
__author__ = "Realtor Agent Team"

from .core import (
    Config,
    config,
    RealtorOrchestrator,
    get_logger,
    init_db,
    get_db,
)

from .analytics import (
    DealScorer,
    deal_scorer,
    LeadConversionTracker,
    MarketTrendAnalyzer,
)

from .automation import (
    Workflow,
    WorkflowLibrary,
    workflow_library,
    scheduled_task_manager,
    notification_service,
)

from .integrations import (
    email_service,
    calendar_service,
    crm_integration,
)

__all__ = [
    "__version__",
    "__author__",
    "Config",
    "config",
    "RealtorOrchestrator",
    "get_logger",
    "init_db",
    "get_db",
    "DealScorer",
    "deal_scorer",
    "LeadConversionTracker",
    "MarketTrendAnalyzer",
    "Workflow",
    "WorkflowLibrary",
    "workflow_library",
    "scheduled_task_manager",
    "notification_service",
    "email_service",
    "calendar_service",
    "crm_integration",
]
