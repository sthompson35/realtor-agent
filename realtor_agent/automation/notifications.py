from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum
from ..core.logger import get_logger
from ..core.database import SessionLocal

logger = get_logger(__name__)


class NotificationType(Enum):
    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"


class NotificationChannel(Enum):
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"
    IN_APP = "in_app"


class Notification:
    """Represents a notification"""

    def __init__(
        self,
        user_id: int,
        title: str,
        message: str,
        notification_type: NotificationType = NotificationType.INFO,
        channels: List[NotificationChannel] = None,
        metadata: Dict[str, Any] = None,
    ):
        self.user_id = user_id
        self.title = title
        self.message = message
        self.notification_type = notification_type
        self.channels = channels or [NotificationChannel.IN_APP]
        self.metadata = metadata or {}
        self.created_at = datetime.utcnow()
        self.sent = False
        self.read = False


class NotificationService:
    """Notification service for multi-channel notifications"""

    def __init__(self):
        self.notifications: List[Notification] = []

    def send_notification(
        self,
        user_id: int,
        title: str,
        message: str,
        notification_type: NotificationType = NotificationType.INFO,
        channels: List[NotificationChannel] = None,
        metadata: Dict[str, Any] = None,
    ) -> bool:
        """Send a notification through specified channels"""
        notification = Notification(
            user_id=user_id,
            title=title,
            message=message,
            notification_type=notification_type,
            channels=channels,
            metadata=metadata,
        )

        try:
            for channel in notification.channels:
                if channel == NotificationChannel.EMAIL:
                    self._send_email(notification)
                elif channel == NotificationChannel.SMS:
                    self._send_sms(notification)
                elif channel == NotificationChannel.PUSH:
                    self._send_push(notification)
                elif channel == NotificationChannel.IN_APP:
                    self._send_in_app(notification)

            notification.sent = True
            self.notifications.append(notification)

            logger.info(f"Notification sent to user {user_id}: {title}")
            return True
        except Exception as e:
            logger.error(f"Failed to send notification: {e}")
            return False

    def _send_email(self, notification: Notification):
        """Send email notification"""
        from ..integrations.services import email_service
        from ..core.database import User, SessionLocal

        db = SessionLocal()
        try:
            user = db.query(User).filter(User.id == notification.user_id).first()
            if user and user.email:
                email_service.send_email(to_emails=[user.email], subject=notification.title, body=notification.message)
        finally:
            db.close()

    def _send_sms(self, notification: Notification):
        """Send SMS notification"""
        # TODO: Implement SMS service (Twilio, etc.)
        logger.info(f"SMS notification: {notification.title}")

    def _send_push(self, notification: Notification):
        """Send push notification"""
        # TODO: Implement push notification service (Firebase, etc.)
        logger.info(f"Push notification: {notification.title}")

    def _send_in_app(self, notification: Notification):
        """Store in-app notification"""
        # TODO: Store in database for in-app display
        logger.info(f"In-app notification: {notification.title}")

    def get_user_notifications(self, user_id: int, unread_only: bool = False) -> List[Notification]:
        """Get notifications for a user"""
        notifications = [n for n in self.notifications if n.user_id == user_id]

        if unread_only:
            notifications = [n for n in notifications if not n.read]

        return sorted(notifications, key=lambda x: x.created_at, reverse=True)

    def mark_as_read(self, user_id: int, notification_index: int):
        """Mark a notification as read"""
        user_notifications = self.get_user_notifications(user_id)
        if 0 <= notification_index < len(user_notifications):
            user_notifications[notification_index].read = True
            return True
        return False


class NotificationTemplates:
    """Pre-defined notification templates"""

    @staticmethod
    def new_lead(lead_data: Dict[str, Any]) -> Dict[str, str]:
        """Template for new lead notification"""
        return {
            "title": "New Lead Received",
            "message": f"New lead: {lead_data.get('name')} from {lead_data.get('source')}",
        }

    @staticmethod
    def appointment_reminder(appointment_data: Dict[str, Any]) -> Dict[str, str]:
        """Template for appointment reminder"""
        return {
            "title": "Upcoming Appointment",
            "message": f"Reminder: {appointment_data.get('title')} at {appointment_data.get('scheduled_at')}",
        }

    @staticmethod
    def deal_update(deal_data: Dict[str, Any]) -> Dict[str, str]:
        """Template for deal update notification"""
        return {
            "title": "Deal Update",
            "message": f"Deal {deal_data.get('title')} status changed to {deal_data.get('status')}",
        }

    @staticmethod
    def bot_completed(bot_name: str, results: Dict[str, Any]) -> Dict[str, str]:
        """Template for bot completion notification"""
        return {
            "title": "Bot Completed",
            "message": f"Bot {bot_name} completed. Processed {results.get('items_processed', 0)} items.",
        }

    @staticmethod
    def goal_achieved(goal_data: Dict[str, Any]) -> Dict[str, str]:
        """Template for goal achievement notification"""
        return {
            "title": "Goal Achieved!",
            "message": f"Congratulations! You've achieved your goal: {goal_data.get('title')}",
        }

    @staticmethod
    def system_alert(alert_message: str) -> Dict[str, str]:
        """Template for system alert"""
        return {"title": "System Alert", "message": alert_message}


# Global notification service
notification_service = NotificationService()
notification_templates = NotificationTemplates()
