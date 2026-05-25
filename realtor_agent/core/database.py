# Re-export the canonical models and session factory from models.py.
# This module is kept for backwards-compatibility with existing imports.

from realtor_agent.core.models import (  # noqa: F401
    Base,
    User,
    DealIntakeModel,
    UnderwritingResultModel,
    RehabScopeModel,
    ClosedDealModel,
    Contact,
    OutreachLog,
    BotRun,
    Document,
    Notification,
    engine,
    SessionLocal,
    init_db,
    get_db,
)
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from datetime import datetime as _dt

# ---------------------------------------------------------------------------
# Backward-compatibility aliases — old code uses these names
# ---------------------------------------------------------------------------

# Lead, Property, Deal all map to DealIntakeModel (unified intake table)
Lead = DealIntakeModel
Property = DealIntakeModel
Deal = DealIntakeModel


class Activity(Base):
    """CRM activity / event log — retained for backwards-compatibility."""
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True)
    deal_id_fk = Column(Integer, ForeignKey("deal_intakes.id"), nullable=True)
    activity_type = Column(String(50), nullable=False)
    description = Column(Text)
    outcome = Column(String(50))
    metadata_ = Column("metadata", JSON)
    created_at = Column(DateTime, default=_dt.utcnow)


class Appointment(Base):
    """Appointment / showing record — retained for backwards-compatibility."""
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True)
    deal_id_fk = Column(Integer, ForeignKey("deal_intakes.id"), nullable=True)
    title = Column(String(200))
    description = Column(Text)
    scheduled_at = Column(DateTime)
    duration_minutes = Column(Integer, default=60)
    status = Column(String(20), default="scheduled")
    location = Column(String(200))
    created_at = Column(DateTime, default=_dt.utcnow)
    updated_at = Column(DateTime, default=_dt.utcnow, onupdate=_dt.utcnow)


# ---------------------------------------------------------------------------
# Database helper class — bots instantiate Database(config) for convenience
# ---------------------------------------------------------------------------

class Database:
    """
    Thin wrapper around SessionLocal.
    Bots call Database(config) to get a session-managed db handle.
    """

    def __init__(self, config=None):
        self.config = config
        self._session = None

    def get_session(self):
        if self._session is None:
            self._session = SessionLocal()
        return self._session

    def close(self):
        if self._session:
            self._session.close()
            self._session = None

    def __enter__(self):
        return self.get_session()

    def __exit__(self, *_):
        self.close()
