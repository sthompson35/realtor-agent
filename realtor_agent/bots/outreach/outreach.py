"""
Outreach Bot — Bot 6: Outreach & Follow-Up.
Generates personalised outreach messages for discovered owner contacts
and logs them to the OutreachLog table.
"""

from __future__ import annotations
import logging
import random
from datetime import datetime
from typing import Any

from realtor_agent.bots.base import BaseBot, BotResult
from realtor_agent.core.models import OutreachLog, SessionLocal

logger = logging.getLogger(__name__)

# Message templates per channel
_SMS_TEMPLATES = [
    "Hi {name}, I came across your property at {address} and wanted to reach out. I buy homes as-is, quick close, no hassle. Would you be open to a conversation? — STLLC",
    "Hello {name}! Saw your property on {address}. We're local investors looking for homes in the area. Cash offer, fast close. Interested? Text back anytime. — STLLC",
    "Hi {name}, I'm interested in {address}. We close in 14 days, no repairs needed. Quick call to chat? — STLLC",
]

_EMAIL_SUBJECTS = [
    "Quick question about {address}",
    "Cash offer for {address} — no repairs needed",
    "Interested in your property at {address}",
]

_EMAIL_BODIES = [
    """Hi {name},

I hope this message finds you well. My name is Shylow Thompson with STLLC, a local real estate investment company.

I came across your property at {address} and wanted to reach out directly to see if you'd be open to a conversation about selling.

We offer:
• Cash purchase — no bank delays
• Close in as few as 14 days
• Buy as-is — no repairs needed
• No agent commissions

There's no obligation and no pressure. If the timing isn't right, we completely understand.

Would you be open to a quick 5-minute call to discuss?

Best regards,
Shylow Thompson
STLLC Investments
""",
]


def _generate_message(contact: dict, channel: str) -> str:
    name    = contact.get("name", "there")
    address = contact.get("address", "your property")
    rng     = random.Random(contact.get("deal_id", "") + channel)

    if channel == "sms":
        return rng.choice(_SMS_TEMPLATES).format(name=name.split()[0], address=address)
    subject = rng.choice(_EMAIL_SUBJECTS).format(address=address)
    body    = rng.choice(_EMAIL_BODIES).format(name=name.split()[0], address=address)
    return f"Subject: {subject}\n\n{body}"


class OutreachBot(BaseBot):
    """
    Bot 6 — Outreach & Follow-Up.

    Reads owner contacts from context["owner_finder"]["contacts"],
    generates personalised outreach messages (SMS + email), and
    logs each attempt to OutreachLog.

    Context in:  context["owner_finder"]["contacts"]
    Context out: context["outreach"]["sent"]
    """

    name = "outreach"

    def __init__(self, config=None, database=None, **kwargs):
        self.config = config

    def run(self, context: dict) -> BotResult:
        contacts: list[dict] = context.get("owner_finder", {}).get("contacts", [])

        if not contacts:
            logger.info("Outreach: no contacts to reach")
            return BotResult({"sent": 0, "messages": []})

        db = SessionLocal()
        messages: list[dict[str, Any]] = []

        try:
            for contact in contacts:
                for channel in ("sms", "email"):
                    # Skip email if no address; skip sms if no phone
                    if channel == "email" and not contact.get("email"):
                        continue
                    if channel == "sms" and not contact.get("phone"):
                        continue

                    body = _generate_message(contact, channel)
                    deal_fk = contact.get("_db_id")
                    if not deal_fk:
                        continue  # OutreachLog requires a valid deal FK
                    log  = OutreachLog(
                        deal_id_fk    = deal_fk,
                        channel       = channel,
                        direction     = "outbound",
                        message       = body,
                        sent_at       = datetime.utcnow(),
                        campaign_type = "initial",
                    )
                    db.add(log)
                    messages.append({
                        "contact": contact.get("name"),
                        "channel": channel,
                        "address": contact.get("address"),
                        "status":  "queued",
                    })

            db.commit()
        except Exception as exc:
            db.rollback()
            logger.error("Outreach DB error: %s", exc)
        finally:
            db.close()

        logger.info("Outreach: %d messages queued", len(messages))
        return BotResult({"sent": len(messages), "messages": messages})
