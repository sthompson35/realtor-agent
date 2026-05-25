from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from sqlalchemy import func
from ..core.database import Lead, Activity, Appointment, Deal, SessionLocal
from ..core.logger import get_logger

logger = get_logger(__name__)


class LeadConversionTracker:
    """Track and analyze lead conversion metrics"""

    def __init__(self):
        self.conversion_stages = [
            "new",
            "contacted",
            "qualified",
            "appointment_set",
            "appointment_completed",
            "offer_made",
            "under_contract",
            "closed",
        ]

    def track_conversion(self, lead_id: int, stage: str, metadata: Dict = None):
        """Track a lead conversion event"""
        db = SessionLocal()
        try:
            lead = db.query(Lead).filter(Lead.id == lead_id).first()
            if not lead:
                logger.warning(f"Lead not found: {lead_id}")
                return False

            # Update lead status
            lead.status = stage
            lead.updated_at = datetime.utcnow()

            # Create activity record
            activity = Activity(
                lead_id=lead_id,
                activity_type="status_change",
                description=f"Lead moved to {stage}",
                metadata=metadata or {},
            )

            db.add(activity)
            db.commit()

            logger.info(f"Lead {lead_id} converted to {stage}")
            return True
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to track conversion: {e}")
            return False
        finally:
            db.close()

    def get_conversion_funnel(self, start_date: datetime = None, end_date: datetime = None) -> Dict[str, Any]:
        """Get conversion funnel metrics"""
        db = SessionLocal()
        try:
            query = db.query(Lead.status, func.count(Lead.id))

            if start_date:
                query = query.filter(Lead.created_at >= start_date)
            if end_date:
                query = query.filter(Lead.created_at <= end_date)

            results = query.group_by(Lead.status).all()

            funnel = {stage: 0 for stage in self.conversion_stages}
            total = 0

            for status, count in results:
                if status in funnel:
                    funnel[status] = count
                    total += count

            # Calculate conversion rates
            conversion_rates = {}
            for i, stage in enumerate(self.conversion_stages[:-1]):
                next_stage = self.conversion_stages[i + 1]
                if funnel[stage] > 0:
                    conversion_rates[f"{stage}_to_{next_stage}"] = funnel[next_stage] / funnel[stage] * 100

            return {"funnel": funnel, "total_leads": total, "conversion_rates": conversion_rates}
        finally:
            db.close()

    def get_lead_velocity(self, lead_id: int) -> Dict[str, Any]:
        """Calculate time spent in each stage"""
        db = SessionLocal()
        try:
            activities = (
                db.query(Activity)
                .filter(Activity.lead_id == lead_id, Activity.activity_type == "status_change")
                .order_by(Activity.created_at)
                .all()
            )

            if not activities:
                return {}

            velocity = {}
            for i in range(len(activities) - 1):
                current = activities[i]
                next_activity = activities[i + 1]

                time_diff = (next_activity.created_at - current.created_at).total_seconds() / 3600
                stage = current.description.replace("Lead moved to ", "")
                velocity[stage] = time_diff

            return velocity
        finally:
            db.close()

    def get_conversion_metrics(self, days: int = 30) -> Dict[str, Any]:
        """Get overall conversion metrics"""
        db = SessionLocal()
        try:
            start_date = datetime.utcnow() - timedelta(days=days)

            total_leads = db.query(func.count(Lead.id)).filter(Lead.created_at >= start_date).scalar()

            converted_leads = (
                db.query(func.count(Lead.id))
                .filter(Lead.created_at >= start_date, Lead.status.in_(["closed", "under_contract"]))
                .scalar()
            )

            avg_conversion_time = (
                db.query(func.avg(func.julianday(Lead.updated_at) - func.julianday(Lead.created_at)))
                .filter(Lead.created_at >= start_date, Lead.status == "closed")
                .scalar()
            )

            conversion_rate = (converted_leads / total_leads * 100) if total_leads > 0 else 0

            return {
                "period_days": days,
                "total_leads": total_leads,
                "converted_leads": converted_leads,
                "conversion_rate": round(conversion_rate, 2),
                "avg_conversion_time_days": round(avg_conversion_time or 0, 1),
            }
        finally:
            db.close()

    def get_source_performance(self, days: int = 30) -> List[Dict[str, Any]]:
        """Analyze lead source performance"""
        db = SessionLocal()
        try:
            start_date = datetime.utcnow() - timedelta(days=days)

            results = (
                db.query(
                    Lead.source,
                    func.count(Lead.id).label("total"),
                    func.sum(func.case([(Lead.status == "closed", 1)], else_=0)).label("converted"),
                )
                .filter(Lead.created_at >= start_date)
                .group_by(Lead.source)
                .all()
            )

            performance = []
            for source, total, converted in results:
                conversion_rate = (converted / total * 100) if total > 0 else 0
                performance.append(
                    {
                        "source": source,
                        "total_leads": total,
                        "converted_leads": converted,
                        "conversion_rate": round(conversion_rate, 2),
                    }
                )

            return sorted(performance, key=lambda x: x["conversion_rate"], reverse=True)
        finally:
            db.close()


# Global lead conversion tracker instance
lead_conversion_tracker = LeadConversionTracker()
