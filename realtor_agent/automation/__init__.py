"""
Automation modules for workflows, scheduling, and notifications.
"""

from .workflow import Workflow, WorkflowStep, WorkflowStatus, WorkflowLibrary, workflow_library
from .scheduler import ScheduledTaskManager, DefaultScheduledTasks, scheduled_task_manager
from .notifications import (
    Notification,
    NotificationService,
    NotificationType,
    NotificationChannel,
    NotificationTemplates,
    notification_service,
    notification_templates,
)

__all__ = [
    "Workflow",
    "WorkflowStep",
    "WorkflowStatus",
    "WorkflowLibrary",
    "workflow_library",
    "ScheduledTaskManager",
    "DefaultScheduledTasks",
    "scheduled_task_manager",
    "Notification",
    "NotificationService",
    "NotificationType",
    "NotificationChannel",
    "NotificationTemplates",
    "notification_service",
    "notification_templates",
]
