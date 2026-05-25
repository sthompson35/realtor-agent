"""
Database migration script for Realtor Agent
Run this to create or update database schema
"""

from realtor_agent.core.database import init_db, engine, Base
from realtor_agent.core.logger import get_logger

logger = get_logger(__name__)


def run_migrations():
    """Run database migrations"""
    try:
        logger.info("Starting database migrations...")
        init_db()
        logger.info("Database migrations completed successfully")
        return True
    except Exception as e:
        logger.error(f"Database migration failed: {e}")
        return False


if __name__ == "__main__":
    run_migrations()
