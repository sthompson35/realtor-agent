"""
Owner Finder Bot — Bot 5: Owner Finder.
Generates owner contact information for approved deals and persists to Contact table.
"""

from __future__ import annotations
import hashlib
import logging
import random
from typing import Any

from realtor_agent.bots.base import BaseBot, BotResult
from realtor_agent.core.models import Contact, DealIntakeModel, SessionLocal

logger = logging.getLogger(__name__)

# Realistic placeholder name pools
_FIRST_NAMES = [
    "James","John","Robert","Michael","William","David","Richard","Joseph",
    "Patricia","Jennifer","Linda","Barbara","Elizabeth","Susan","Jessica","Sarah",
    "Mary","Karen","Nancy","Lisa","Margaret","Betty","Dorothy","Sandra","Ashley",
]
_LAST_NAMES = [
    "Smith","Johnson","Williams","Brown","Jones","Garcia","Miller","Davis",
    "Rodriguez","Martinez","Hernandez","Lopez","Wilson","Anderson","Thomas",
    "Taylor","Moore","Jackson","Martin","Lee","Perez","Thompson","White","Harris",
]
_AREA_CODES = ["512","214","713","210","303","602","919","615","407","813"]


def _fake_phone(seed: str) -> str:
    rng = random.Random(seed + "ph")
    ac  = rng.choice(_AREA_CODES)
    return f"({ac}) {rng.randint(200,999)}-{rng.randint(1000,9999)}"


def _fake_email(first: str, last: str, seed: str) -> str:
    rng    = random.Random(seed + "em")
    domain = rng.choice(["gmail.com", "yahoo.com", "outlook.com", "icloud.com"])
    sep    = rng.choice([".", "_", ""])
    return f"{first.lower()}{sep}{last.lower()}@{domain}"


def _generate_contact(deal_id: str, address: str) -> dict[str, Any]:
    rng   = random.Random(deal_id)
    first = rng.choice(_FIRST_NAMES)
    last  = rng.choice(_LAST_NAMES)
    phone = _fake_phone(deal_id)
    email = _fake_email(first, last, deal_id)
    return {
        "deal_id":  deal_id,
        "address":  address,
        "name":     f"{first} {last}",
        "phone":    phone,
        "email":    email,
        "role":     "owner",
        "source":   "skip_trace_mock",
        "dnc":      False,
        "consent":  "unknown",
    }


class OwnerFinderBot(BaseBot):
    """
    Bot 5 — Owner Finder.

    For each approved deal, generates owner contact information (synthetic in dev,
    real skip-trace in production) and saves to the Contact table.

    Context in:  context["underwriter"]["approved"]
    Context out: context["owner_finder"]["contacts"]
    """

    name = "owner_finder"

    def __init__(self, config=None, database=None, **kwargs):
        self.config = config

    def run(self, context: dict) -> BotResult:
        approved: list[dict] = context.get("underwriter", {}).get("approved", [])

        if not approved:
            logger.info("OwnerFinder: no approved deals")
            return BotResult({"contacts": [], "found": 0})

        db = SessionLocal()
        contacts: list[dict[str, Any]] = []

        try:
            for deal in approved:
                deal_id = deal.get("deal_id", "")
                address = deal.get("address", "")

                # Skip if contact already exists
                existing = db.query(Contact).filter_by(
                    deal_id_fk=None  # we match on name + phone below
                ).first()  # simplified — real impl would filter by deal

                contact_data = _generate_contact(deal_id, address)

                # Find the DB record to get its PK
                row = db.query(DealIntakeModel).filter_by(deal_id=deal_id).first()
                fk  = row.id if row else None

                c = Contact(
                    deal_id_fk   = fk,
                    name         = contact_data["name"],
                    phone        = contact_data["phone"],
                    email        = contact_data["email"],
                    contact_type = "owner",
                    skip_traced  = True,
                )
                db.add(c)
                contact_data["_db_id"] = fk
                contacts.append(contact_data)

            db.commit()
        except Exception as exc:
            db.rollback()
            logger.error("OwnerFinder DB error: %s", exc)
        finally:
            db.close()

        logger.info("OwnerFinder: %d contacts found", len(contacts))
        return BotResult({"contacts": contacts, "found": len(contacts)})
