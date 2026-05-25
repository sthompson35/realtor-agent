import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Optional
from ..core.config import config
from ..core.logger import get_logger

logger = get_logger(__name__)


class EmailService:
    """Email service integration"""

    def __init__(self):
        self.smtp_host = config.get("email.smtp_host", "smtp.gmail.com")
        self.smtp_port = config.get("email.smtp_port", 587)
        self.smtp_user = config.get("email.smtp_user")
        self.smtp_password = config.get("email.smtp_password")
        self.from_email = config.get("email.from_email")
        self.from_name = config.get("email.from_name", "Realtor Agent")

    def send_email(
        self,
        to_emails: List[str],
        subject: str,
        body: str,
        html_body: Optional[str] = None,
        cc: List[str] = None,
        bcc: List[str] = None,
    ) -> bool:
        """Send an email"""
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = f"{self.from_name} <{self.from_email}>"
            msg["To"] = ", ".join(to_emails)

            if cc:
                msg["Cc"] = ", ".join(cc)

            # Attach plain text
            msg.attach(MIMEText(body, "plain"))

            # Attach HTML if provided
            if html_body:
                msg.attach(MIMEText(html_body, "html"))

            # Connect to SMTP server
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)

                recipients = to_emails + (cc or []) + (bcc or [])
                server.send_message(msg, self.from_email, recipients)

            logger.info(f"Email sent to {to_emails}")
            return True
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return False

    def send_lead_notification(self, lead_data: dict) -> bool:
        """Send notification for new lead"""
        subject = f"New Lead: {lead_data.get('name')}"
        body = f"""
        New lead received:
        
        Name: {lead_data.get('name')}
        Email: {lead_data.get('email')}
        Phone: {lead_data.get('phone')}
        Source: {lead_data.get('source')}
        
        View in dashboard: {config.get('app.base_url')}/leads/{lead_data.get('id')}
        """

        recipients = config.get("email.notification_recipients", [])
        return self.send_email(recipients, subject, body)

    def send_appointment_reminder(self, appointment_data: dict) -> bool:
        """Send appointment reminder"""
        subject = f"Appointment Reminder: {appointment_data.get('title')}"
        body = f"""
        Reminder: You have an upcoming appointment
        
        Title: {appointment_data.get('title')}
        Date: {appointment_data.get('scheduled_at')}
        Location: {appointment_data.get('location')}
        
        View details: {config.get('app.base_url')}/appointments/{appointment_data.get('id')}
        """

        recipients = [appointment_data.get("lead_email")]
        return self.send_email(recipients, subject, body)


class CalendarService:
    """Calendar integration service"""

    def __init__(self):
        self.calendar_type = config.get("calendar.type", "google")
        self.api_key = config.get("calendar.api_key")

    def create_event(self, event_data: dict) -> Optional[str]:
        """Create a calendar event"""
        try:
            # TODO: Implement actual calendar API integration
            logger.info(f"Creating calendar event: {event_data.get('title')}")

            # Mock event ID
            event_id = f"event_{event_data.get('id')}"

            return event_id
        except Exception as e:
            logger.error(f"Failed to create calendar event: {e}")
            return None

    def update_event(self, event_id: str, event_data: dict) -> bool:
        """Update a calendar event"""
        try:
            logger.info(f"Updating calendar event: {event_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to update calendar event: {e}")
            return False

    def delete_event(self, event_id: str) -> bool:
        """Delete a calendar event"""
        try:
            logger.info(f"Deleting calendar event: {event_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete calendar event: {e}")
            return False


class CRMIntegration:
    """CRM integration framework"""

    def __init__(self):
        self.crm_type = config.get("crm.type")
        self.api_key = config.get("crm.api_key")
        self.api_url = config.get("crm.api_url")

    def sync_lead(self, lead_data: dict) -> bool:
        """Sync lead to CRM"""
        try:
            logger.info(f"Syncing lead to CRM: {lead_data.get('id')}")

            # TODO: Implement actual CRM API integration
            # Example for Salesforce, HubSpot, Pipedrive, etc.

            return True
        except Exception as e:
            logger.error(f"Failed to sync lead to CRM: {e}")
            return False

    def sync_deal(self, deal_data: dict) -> bool:
        """Sync deal to CRM"""
        try:
            logger.info(f"Syncing deal to CRM: {deal_data.get('id')}")
            return True
        except Exception as e:
            logger.error(f"Failed to sync deal to CRM: {e}")
            return False

    def sync_contact(self, contact_data: dict) -> bool:
        """Sync contact to CRM"""
        try:
            logger.info(f"Syncing contact to CRM: {contact_data.get('id')}")
            return True
        except Exception as e:
            logger.error(f"Failed to sync contact to CRM: {e}")
            return False

    def get_crm_data(self, entity_type: str, entity_id: str) -> Optional[dict]:
        """Get data from CRM"""
        try:
            logger.info(f"Fetching {entity_type} from CRM: {entity_id}")

            # TODO: Implement actual CRM API call

            return None
        except Exception as e:
            logger.error(f"Failed to get CRM data: {e}")
            return None


# Global service instances
email_service = EmailService()
calendar_service = CalendarService()
crm_integration = CRMIntegration()
