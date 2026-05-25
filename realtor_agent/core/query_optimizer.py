from sqlalchemy import Index
from sqlalchemy.orm import Query
from typing import List, Dict, Any
from ..core.database import Base, Lead, Property, Deal, Appointment
from ..core.logger import get_logger

logger = get_logger(__name__)


class QueryOptimizer:
    """Database query optimization utilities"""

    @staticmethod
    def create_indexes():
        """Create database indexes for common queries"""
        indexes = [
            # Lead indexes
            Index("idx_lead_status", Lead.status),
            Index("idx_lead_source", Lead.source),
            Index("idx_lead_created_at", Lead.created_at),
            Index("idx_lead_score", Lead.score),
            # Property indexes
            Index("idx_property_city_state", Property.city, Property.state),
            Index("idx_property_price", Property.price),
            Index("idx_property_status", Property.status),
            Index("idx_property_deal_score", Property.deal_score),
            # Deal indexes
            Index("idx_deal_status", Deal.status),
            Index("idx_deal_stage", Deal.stage),
            Index("idx_deal_value", Deal.value),
            # Appointment indexes
            Index("idx_appointment_scheduled_at", Appointment.scheduled_at),
            Index("idx_appointment_status", Appointment.status),
        ]

        logger.info(f"Created {len(indexes)} database indexes")
        return indexes

    @staticmethod
    def optimize_lead_query(query: Query, filters: Dict[str, Any] = None) -> Query:
        """Optimize lead queries with common patterns"""
        if not filters:
            return query

        # Apply filters efficiently
        if "status" in filters:
            query = query.filter(Lead.status == filters["status"])

        if "source" in filters:
            query = query.filter(Lead.source == filters["source"])

        if "min_score" in filters:
            query = query.filter(Lead.score >= filters["min_score"])

        if "created_after" in filters:
            query = query.filter(Lead.created_at >= filters["created_after"])

        return query

    @staticmethod
    def optimize_property_query(query: Query, filters: Dict[str, Any] = None) -> Query:
        """Optimize property queries with common patterns"""
        if not filters:
            return query

        # Apply filters efficiently
        if "city" in filters:
            query = query.filter(Property.city == filters["city"])

        if "state" in filters:
            query = query.filter(Property.state == filters["state"])

        if "min_price" in filters:
            query = query.filter(Property.price >= filters["min_price"])

        if "max_price" in filters:
            query = query.filter(Property.price <= filters["max_price"])

        if "status" in filters:
            query = query.filter(Property.status == filters["status"])

        if "min_deal_score" in filters:
            query = query.filter(Property.deal_score >= filters["min_deal_score"])

        return query

    @staticmethod
    def paginate(query: Query, page: int = 1, per_page: int = 20) -> Dict[str, Any]:
        """Paginate query results efficiently"""
        total = query.count()
        items = query.offset((page - 1) * per_page).limit(per_page).all()

        return {
            "items": items,
            "total": total,
            "page": page,
            "per_page": per_page,
            "pages": (total + per_page - 1) // per_page,
        }


# Initialize indexes on import
query_optimizer = QueryOptimizer()
