from celery import Celery
from ..core.config import config
from ..core.logger import get_logger

logger = get_logger(__name__)

# Initialize Celery app
celery_app = Celery(
    "realtor_agent", broker=config.get("celery.broker_url"), backend=config.get("celery.result_backend")
)

# Celery configuration
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,
    task_soft_time_limit=25 * 60,
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
)


@celery_app.task(name="realtor_agent.tasks.run_bot")
def run_bot_task(bot_name: str, params: dict = None):
    """Async task to run a bot"""
    from ..bots.error_handling import RetryStrategy, BotErrorHandler
    from ..bots.state_manager import bot_state_manager

    logger.info(f"Starting bot task: {bot_name}")

    try:
        # Load bot state for context seeding
        state = bot_state_manager.load_state(bot_name)

        from realtor_agent.core.orchestrator import Orchestrator
        from realtor_agent.core.config import load_config

        orch = Orchestrator(bot_names=[bot_name], config=load_config())
        if params:
            orch.context.update(params)

        results = orch.run()
        result  = dict(results[0]) if results else {}
        result.setdefault("bot_name", bot_name)
        result.setdefault("status", "completed")

        bot_state_manager.save_state(bot_name, result)
        logger.info(f"Bot task completed: {bot_name}")
        return result
    except Exception as e:
        logger.error(f"Bot task failed: {bot_name} - {e}")
        BotErrorHandler.handle_error(bot_name, e)
        raise


@celery_app.task(name="realtor_agent.tasks.process_lead")
def process_lead_task(lead_id: int):
    """Async task to process a lead"""
    from ..core.database import Lead, SessionLocal
    from ..analytics.deal_scoring import deal_scorer

    logger.info(f"Processing lead: {lead_id}")

    db = SessionLocal()
    try:
        lead = db.query(Lead).filter(Lead.id == lead_id).first()
        if not lead:
            logger.warning(f"Lead not found: {lead_id}")
            return None

        # Calculate lead score
        # TODO: Implement actual lead scoring logic
        lead.score = 0.75

        db.commit()

        logger.info(f"Lead processed: {lead_id}")
        return {"lead_id": lead_id, "score": lead.score}
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to process lead: {e}")
        raise
    finally:
        db.close()


@celery_app.task(name="realtor_agent.tasks.send_notification")
def send_notification_task(user_id: int, message: str, notification_type: str = "info"):
    """Async task to send a notification"""
    logger.info(f"Sending notification to user {user_id}: {message}")

    # TODO: Implement actual notification sending (email, SMS, push)

    return {"user_id": user_id, "message": message, "type": notification_type, "sent": True}


@celery_app.task(name="realtor_agent.tasks.generate_report")
def generate_report_task(report_type: str, params: dict = None):
    """Async task to generate a report"""
    logger.info(f"Generating report: {report_type}")

    # TODO: Implement actual report generation

    return {"report_type": report_type, "status": "completed", "file_path": f"/reports/{report_type}.pdf"}


@celery_app.task(name="realtor_agent.tasks.cleanup_old_data")
def cleanup_old_data_task(days: int = 90):
    """Async task to cleanup old data"""
    from datetime import datetime, timedelta
    from ..core.database import Activity, SessionLocal

    logger.info(f"Cleaning up data older than {days} days")

    db = SessionLocal()
    try:
        cutoff_date = datetime.utcnow() - timedelta(days=days)

        deleted = db.query(Activity).filter(Activity.created_at < cutoff_date).delete()

        db.commit()

        logger.info(f"Cleaned up {deleted} old records")
        return {"deleted_records": deleted}
    except Exception as e:
        db.rollback()
        logger.error(f"Cleanup failed: {e}")
        raise
    finally:
        db.close()
