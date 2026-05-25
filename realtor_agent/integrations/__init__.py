"""
Integration services for email, calendar, and CRM.
"""

from .services import (
    EmailService,
    CalendarService,
    CRMIntegration,
    email_service,
    calendar_service,
    crm_integration,
)

__all__ = [
    "EmailService",
    "CalendarService",
    "CRMIntegration",
    "email_service",
    "calendar_service",
    "crm_integration",
]
