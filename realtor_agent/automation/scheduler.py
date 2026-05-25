from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime
from typing import Callable, Dict, Any
from ..core.logger import get_logger

logger = get_logger(__name__)


class ScheduledTaskManager:
    """Manage scheduled tasks and cron jobs"""

    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.tasks: Dict[str, Dict[str, Any]] = {}

    def start(self):
        """Start the scheduler"""
        if not self.scheduler.running:
            self.scheduler.start()
            logger.info("Scheduled task manager started")

    def stop(self):
        """Stop the scheduler"""
        if self.scheduler.running:
            self.scheduler.shutdown()
            logger.info("Scheduled task manager stopped")

    def add_cron_task(
        self,
        task_id: str,
        func: Callable,
        cron_expression: str = None,
        hour: int = None,
        minute: int = None,
        day_of_week: str = None,
        **kwargs,
    ):
        """Add a cron-based scheduled task"""
        try:
            if cron_expression:
                trigger = CronTrigger.from_crontab(cron_expression)
            else:
                trigger = CronTrigger(hour=hour, minute=minute, day_of_week=day_of_week)

            job = self.scheduler.add_job(func, trigger=trigger, id=task_id, kwargs=kwargs, replace_existing=True)

            self.tasks[task_id] = {
                "type": "cron",
                "function": func.__name__,
                "trigger": str(trigger),
                "next_run": job.next_run_time,
            }

            logger.info(f"Added cron task: {task_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to add cron task: {e}")
            return False

    def add_interval_task(
        self, task_id: str, func: Callable, seconds: int = None, minutes: int = None, hours: int = None, **kwargs
    ):
        """Add an interval-based scheduled task"""
        try:
            interval_kwargs = {k: v for k, v in {"seconds": seconds, "minutes": minutes, "hours": hours}.items() if v is not None}
            trigger = IntervalTrigger(**interval_kwargs)

            job = self.scheduler.add_job(func, trigger=trigger, id=task_id, kwargs=kwargs, replace_existing=True)

            self.tasks[task_id] = {
                "type": "interval",
                "function": func.__name__,
                "trigger": str(trigger),
                "next_run": job.next_run_time,
            }

            logger.info(f"Added interval task: {task_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to add interval task: {e}")
            return False

    def remove_task(self, task_id: str):
        """Remove a scheduled task"""
        try:
            self.scheduler.remove_job(task_id)
            if task_id in self.tasks:
                del self.tasks[task_id]
            logger.info(f"Removed task: {task_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to remove task: {e}")
            return False

    def get_tasks(self) -> Dict[str, Dict[str, Any]]:
        """Get all scheduled tasks"""
        return self.tasks

    def pause_task(self, task_id: str):
        """Pause a scheduled task"""
        try:
            self.scheduler.pause_job(task_id)
            logger.info(f"Paused task: {task_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to pause task: {e}")
            return False

    def resume_task(self, task_id: str):
        """Resume a paused task"""
        try:
            self.scheduler.resume_job(task_id)
            logger.info(f"Resumed task: {task_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to resume task: {e}")
            return False


class DefaultScheduledTasks:
    """Default scheduled tasks for the system"""

    @staticmethod
    def setup_default_tasks(scheduler: ScheduledTaskManager):
        """Setup default scheduled tasks"""

        # Daily data cleanup (runs at 2 AM)
        scheduler.add_cron_task("daily_cleanup", DefaultScheduledTasks.cleanup_old_data, hour=2, minute=0)

        # Hourly bot status check
        scheduler.add_interval_task("bot_status_check", DefaultScheduledTasks.check_bot_status, hours=1)

        # Daily lead scoring update (runs at 3 AM)
        scheduler.add_cron_task("daily_lead_scoring", DefaultScheduledTasks.update_lead_scores, hour=3, minute=0)

        # Weekly market data refresh (runs Sunday at 1 AM)
        scheduler.add_cron_task(
            "weekly_market_refresh", DefaultScheduledTasks.refresh_market_data, day_of_week="sun", hour=1, minute=0
        )

        logger.info("Default scheduled tasks configured")

    @staticmethod
    def cleanup_old_data():
        """Cleanup old data"""
        from ..core.tasks import cleanup_old_data_task

        logger.info("Running scheduled cleanup task")
        cleanup_old_data_task.delay(days=90)

    @staticmethod
    def check_bot_status():
        """Check bot status"""
        from ..bots.state_manager import bot_state_manager

        logger.info("Running scheduled bot status check")
        states = bot_state_manager.list_states()
        logger.info(f"Found {len(states)} bot states")

    @staticmethod
    def update_lead_scores():
        """Update lead scores"""
        from ..core.database import Lead, SessionLocal
        from ..analytics.deal_scoring import deal_scorer

        logger.info("Running scheduled lead scoring update")
        db = SessionLocal()
        try:
            leads = db.query(Lead).filter(Lead.status.in_(["new", "contacted"])).all()
            for lead in leads:
                # TODO: Implement actual lead scoring
                lead.score = 0.75
            db.commit()
            logger.info(f"Updated scores for {len(leads)} leads")
        finally:
            db.close()

    @staticmethod
    def refresh_market_data():
        """Refresh market data"""
        logger.info("Running scheduled market data refresh")
        # TODO: Implement market data refresh logic


# Global scheduled task manager
scheduled_task_manager = ScheduledTaskManager()
