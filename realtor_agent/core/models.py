"""
SQLAlchemy models — canonical field vocabulary from system_field_map_v8.xlsx.

Tables:
  users           — authentication
  deal_intakes    — central deal input (mirrors Intake sheet, 34 cols)
  underwriting_results — per-strategy output rows
  rehab_scopes    — rehab line-item snapshots
  closed_deals    — archive (mirrors 10_CLOSED_DEALS_LOG)
  outreach_log    — outreach events
  bot_runs        — pipeline execution history
  leads           — CRM pipeline tracking
  contacts        — owner / vendor contacts
  documents       — file attachments
"""

from __future__ import annotations
from datetime import datetime
from sqlalchemy import (
    Boolean, Column, Date, DateTime, Float, ForeignKey,
    Integer, JSON, String, Text, create_engine,
)
from sqlalchemy.orm import DeclarativeBase, relationship, sessionmaker
import os


class Base(DeclarativeBase):
    pass


# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), default="agent")   # admin | agent | readonly
    is_active = Column(Boolean, default=True)
    failed_login_attempts = Column(Integer, default=0)
    locked_until = Column(DateTime, nullable=True)
    settings_json = Column(JSON, default=dict)   # persistent user preferences
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# ---------------------------------------------------------------------------
# Deal Intake — central deal input (Intake sheet, 34 columns)
# ---------------------------------------------------------------------------

class DealIntakeModel(Base):
    __tablename__ = "deal_intakes"

    id = Column(Integer, primary_key=True)
    deal_id = Column(String(50), unique=True, nullable=False, index=True)

    # Identity
    address = Column(String(200), nullable=False)
    city = Column(String(100))
    state = Column(String(2))
    county = Column(String(100))
    zip_code = Column(String(10))
    asset_type = Column(String(20), default="SFR")  # SFR|MF|Land|Commercial|Duplex|4plex

    # Acquisition
    contract_price = Column(Float, default=0.0)
    arv = Column(Float, default=0.0)
    rehab_cost = Column(Float, default=0.0)
    dom = Column(Integer, default=0)            # Days on market

    # Income
    monthly_rent = Column(Float, default=0.0)

    # Operating expenses
    taxes = Column(Float, default=0.0)          # Annual
    insurance = Column(Float, default=0.0)      # Annual
    hoa = Column(Float, default=0.0)            # Monthly
    opex_other = Column(Float, default=0.0)     # Annual other

    # Expense ratios (decimals)
    vacancy_pct = Column(Float, default=0.08)
    pm_pct = Column(Float, default=0.08)
    repairs_pct = Column(Float, default=0.05)
    capex_pct = Column(Float, default=0.05)

    # Exit / acquisition costs
    sell_cost_pct = Column(Float, default=0.08)
    buy_close_pct = Column(Float, default=0.03)
    hold_months = Column(Integer, default=6)

    # Financing
    rate = Column(Float, default=0.08)
    points = Column(Float, default=0.02)
    down_pct = Column(Float, default=0.20)
    term_years = Column(Integer, default=30)

    # Land-specific
    acres = Column(Float, default=0.0)
    zoning = Column(String(50))
    buildable = Column(Boolean, default=True)
    road_access = Column(Boolean, default=True)
    flood_zone = Column(String(10), default="X")

    # Profit targets (Settings sheet defaults)
    flip_profit_target_pct = Column(Float, default=0.20)
    wholesale_min_fee = Column(Float, default=5000.0)
    investor_margin_pct = Column(Float, default=0.15)

    # Pipeline / CRM
    status = Column(String(30), default="lead")
    # lead | qualified | offer_sent | under_contract | closed | dead
    priority = Column(String(10), default="medium")
    source = Column(String(50))
    assigned_to = Column(String(100))
    notes = Column(Text)

    # Scoring / legacy compat columns
    score = Column(Float, default=0.0)          # Lead quality score
    deal_score = Column(Float, default=0.0)     # Deal quality score
    stage = Column(String(50))                  # Pipeline stage label
    value = Column(Float)                       # Deal/pipeline value
    price = Column(Float)                       # Asking / list price

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    underwriting_results = relationship("UnderwritingResultModel", back_populates="deal", cascade="all, delete-orphan")
    rehab_scopes = relationship("RehabScopeModel", back_populates="deal", cascade="all, delete-orphan")
    outreach_logs = relationship("OutreachLog", back_populates="deal", cascade="all, delete-orphan")
    documents = relationship("Document", back_populates="deal", cascade="all, delete-orphan")


# ---------------------------------------------------------------------------
# Underwriting Results — one row per strategy per deal
# ---------------------------------------------------------------------------

class UnderwritingResultModel(Base):
    __tablename__ = "underwriting_results"

    id = Column(Integer, primary_key=True)
    deal_id_fk = Column(Integer, ForeignKey("deal_intakes.id"), nullable=False, index=True)
    strategy = Column(String(50), nullable=False)   # Fix_and_Flip | BRRRR | etc.
    viable = Column(Boolean, default=False)
    flags = Column(JSON)                            # list of risk flag strings

    # Common outputs
    mao = Column(Float)
    recommended_offer = Column(Float)
    roi = Column(Float)
    noi = Column(Float)
    cap_rate = Column(Float)
    dscr = Column(Float)
    coc_return = Column(Float)
    annual_cash_flow = Column(Float)
    net_profit = Column(Float)
    gross_profit = Column(Float)

    # Full strategy payload stored as JSON for flexibility
    full_result = Column(JSON)

    computed_at = Column(DateTime, default=datetime.utcnow)

    deal = relationship("DealIntakeModel", back_populates="underwriting_results")


# ---------------------------------------------------------------------------
# Rehab Scope snapshots
# ---------------------------------------------------------------------------

class RehabScopeModel(Base):
    __tablename__ = "rehab_scopes"

    id = Column(Integer, primary_key=True)
    deal_id_fk = Column(Integer, ForeignKey("deal_intakes.id"), nullable=False, index=True)
    scope_level = Column(String(10))    # light | medium | heavy
    sqft = Column(Float)
    subtotal = Column(Float)
    contingency_pct = Column(Float)
    contingency_amount = Column(Float)
    total = Column(Float)
    line_items = Column(JSON)           # list of ScopeLineItem dicts
    contractor_bids = Column(JSON)      # BidCompareResult dict
    draw_schedule = Column(JSON)        # DrawScheduleResult dict
    created_at = Column(DateTime, default=datetime.utcnow)

    deal = relationship("DealIntakeModel", back_populates="rehab_scopes")


# ---------------------------------------------------------------------------
# Closed Deals Archive — mirrors 10_CLOSED_DEALS_LOG
# ---------------------------------------------------------------------------

class ClosedDealModel(Base):
    __tablename__ = "closed_deals"

    id = Column(Integer, primary_key=True)
    deal_id = Column(String(50), unique=True, nullable=False, index=True)
    close_date = Column(Date)
    exit_date = Column(Date)
    market = Column(String(100))
    strategy = Column(String(50))
    entity = Column(String(100))
    status = Column(String(30), default="Closed")

    # Projected
    proj_purchase = Column(Float, default=0.0)
    proj_rehab = Column(Float, default=0.0)
    proj_exit = Column(Float, default=0.0)
    proj_rent = Column(Float, default=0.0)

    # Actual
    actual_purchase = Column(Float, default=0.0)
    actual_rehab = Column(Float, default=0.0)
    actual_exit = Column(Float, default=0.0)
    actual_rent = Column(Float, default=0.0)

    # Financing
    debt_proceeds = Column(Float, default=0.0)
    equity_in = Column(Float, default=0.0)
    hold_months = Column(Integer, default=0)

    # Computed metrics (stored for dashboard performance)
    gross_profit = Column(Float)
    net_profit = Column(Float)
    roi = Column(Float)
    coc = Column(Float)
    dscr = Column(Float)

    # Variance vs projection
    purchase_variance_pct = Column(Float)
    rehab_variance_pct = Column(Float)
    exit_variance_pct = Column(Float)

    post_mortem_notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# ---------------------------------------------------------------------------
# Contacts (owners, vendors, lenders)
# ---------------------------------------------------------------------------

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True)
    deal_id_fk = Column(Integer, ForeignKey("deal_intakes.id"), nullable=True)
    contact_type = Column(String(20), default="owner")  # owner | lender | vendor | agent
    name = Column(String(100), nullable=False)
    email = Column(String(120))
    phone = Column(String(20))
    mailing_address = Column(String(200))
    ownership_type = Column(String(20))     # individual | llc | trust
    dnc = Column(Boolean, default=False)    # Do Not Contact
    consent_given = Column(Boolean, default=False)
    skip_traced = Column(Boolean, default=False)
    verified_at = Column(DateTime)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# ---------------------------------------------------------------------------
# Outreach Log
# ---------------------------------------------------------------------------

class OutreachLog(Base):
    __tablename__ = "outreach_log"

    id = Column(Integer, primary_key=True)
    deal_id_fk = Column(Integer, ForeignKey("deal_intakes.id"), nullable=False, index=True)
    contact_id = Column(Integer, ForeignKey("contacts.id"), nullable=True)
    channel = Column(String(10))            # sms | email | call | mail
    direction = Column(String(10))          # outbound | inbound
    message = Column(Text)
    response = Column(Text)
    sent_at = Column(DateTime)
    response_at = Column(DateTime)
    compliance_checked = Column(Boolean, default=True)
    campaign_type = Column(String(20))      # initial | follow_up | negotiation

    deal = relationship("DealIntakeModel", back_populates="outreach_logs")


# ---------------------------------------------------------------------------
# Bot Run log
# ---------------------------------------------------------------------------

class BotRun(Base):
    __tablename__ = "bot_runs"

    id = Column(Integer, primary_key=True)
    bot_name = Column(String(100), nullable=False, index=True)
    status = Column(String(20), default="running")  # running | success | failed
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    deals_processed = Column(Integer, default=0)
    results = Column(JSON)
    error_message = Column(Text)
    retry_count = Column(Integer, default=0)


# ---------------------------------------------------------------------------
# Documents
# ---------------------------------------------------------------------------

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True)
    deal_id_fk = Column(Integer, ForeignKey("deal_intakes.id"), nullable=False, index=True)
    document_type = Column(String(50))      # contract | term_sheet | investor_packet | lender_packet | inspection
    file_name = Column(String(255))
    file_path = Column(Text)
    file_size = Column(Integer)
    mime_type = Column(String(100))
    attorney_reviewed = Column(Boolean, default=False)
    uploaded_by = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)

    deal = relationship("DealIntakeModel", back_populates="documents")


# ---------------------------------------------------------------------------
# Notifications
# ---------------------------------------------------------------------------

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # None = system-wide
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    level = Column(String(20), default="info")   # info | success | warning | error
    category = Column(String(50), default="system")  # system | deal | bot | contact | pipeline
    link = Column(String(255))                   # optional deep-link URL
    read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


# ---------------------------------------------------------------------------
# DB engine / session factory
# ---------------------------------------------------------------------------

_DB_URL = os.environ.get("DATABASE_URL", "sqlite:///realtor_agent.db")
engine = create_engine(_DB_URL, echo=False, connect_args={"check_same_thread": False} if "sqlite" in _DB_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db() -> None:
    """Create all tables (idempotent) and apply lightweight column migrations."""
    Base.metadata.create_all(bind=engine)
    # Additive migrations — safe to run repeatedly on SQLite
    _safe_migrations()


def _safe_migrations() -> None:
    """Apply ALTER TABLE statements for columns added after initial schema creation."""
    with engine.connect() as conn:
        # users.settings_json (Phase 4)
        try:
            conn.execute(__import__("sqlalchemy").text(
                "ALTER TABLE users ADD COLUMN settings_json TEXT"
            ))
            conn.commit()
        except Exception:
            pass  # column already exists
        # notifications table is handled by create_all; nothing extra needed


def get_db():
    """FastAPI / Flask dependency — yields a session and closes it after use."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
