from typing import Dict, List, Any, Callable, Optional
from datetime import datetime
from enum import Enum
from ..core.logger import get_logger
from ..core.database import SessionLocal

logger = get_logger(__name__)


class WorkflowStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class WorkflowStep:
    """Represents a single step in a workflow"""

    def __init__(
        self,
        name: str,
        action: Callable,
        params: Dict[str, Any] = None,
        condition: Callable = None,
        on_success: Callable = None,
        on_failure: Callable = None,
    ):
        self.name = name
        self.action = action
        self.params = params or {}
        self.condition = condition
        self.on_success = on_success
        self.on_failure = on_failure
        self.status = WorkflowStatus.PENDING
        self.result = None
        self.error = None

    def should_execute(self, context: Dict[str, Any]) -> bool:
        """Check if step should be executed"""
        if self.condition:
            return self.condition(context)
        return True

    def execute(self, context: Dict[str, Any]) -> Any:
        """Execute the step"""
        try:
            self.status = WorkflowStatus.RUNNING
            logger.info(f"Executing workflow step: {self.name}")

            self.result = self.action(context, **self.params)
            self.status = WorkflowStatus.COMPLETED

            if self.on_success:
                self.on_success(context, self.result)

            return self.result
        except Exception as e:
            self.status = WorkflowStatus.FAILED
            self.error = str(e)
            logger.error(f"Workflow step failed: {self.name} - {e}")

            if self.on_failure:
                self.on_failure(context, e)

            raise


class Workflow:
    """Workflow engine for automating multi-step processes"""

    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description
        self.steps: List[WorkflowStep] = []
        self.status = WorkflowStatus.PENDING
        self.context: Dict[str, Any] = {}
        self.started_at: Optional[datetime] = None
        self.completed_at: Optional[datetime] = None

    def add_step(self, step: WorkflowStep):
        """Add a step to the workflow"""
        self.steps.append(step)
        return self

    def execute(self, initial_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute the workflow"""
        self.context = initial_context or {}
        self.status = WorkflowStatus.RUNNING
        self.started_at = datetime.utcnow()

        logger.info(f"Starting workflow: {self.name}")

        try:
            for step in self.steps:
                if not step.should_execute(self.context):
                    logger.info(f"Skipping step: {step.name}")
                    continue

                result = step.execute(self.context)
                self.context[f"step_{step.name}_result"] = result

            self.status = WorkflowStatus.COMPLETED
            self.completed_at = datetime.utcnow()

            logger.info(f"Workflow completed: {self.name}")
            return self.context
        except Exception as e:
            self.status = WorkflowStatus.FAILED
            self.completed_at = datetime.utcnow()
            logger.error(f"Workflow failed: {self.name} - {e}")
            raise

    def get_status(self) -> Dict[str, Any]:
        """Get workflow status"""
        return {
            "name": self.name,
            "status": self.status.value,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "steps": [{"name": step.name, "status": step.status.value, "error": step.error} for step in self.steps],
        }


class WorkflowLibrary:
    """Pre-defined workflows for common tasks"""

    @staticmethod
    def create_lead_workflow() -> Workflow:
        """Workflow for processing new leads"""
        workflow = Workflow("process_new_lead", "Process and qualify new leads")

        def validate_lead(context, **kwargs):
            lead_data = context.get("lead_data")
            # Validation logic
            return True

        def score_lead(context, **kwargs):
            from ..analytics.deal_scoring import deal_scorer

            lead_data = context.get("lead_data")
            # Scoring logic
            return 0.75

        def send_notification(context, **kwargs):
            from ..integrations.services import email_service

            lead_data = context.get("lead_data")
            return email_service.send_lead_notification(lead_data)

        workflow.add_step(WorkflowStep("validate", validate_lead))
        workflow.add_step(WorkflowStep("score", score_lead))
        workflow.add_step(WorkflowStep("notify", send_notification))

        return workflow

    @staticmethod
    def create_appointment_workflow() -> Workflow:
        """Workflow for scheduling appointments"""
        workflow = Workflow("schedule_appointment", "Schedule and confirm appointments")

        def create_calendar_event(context, **kwargs):
            from ..integrations.services import calendar_service

            appointment_data = context.get("appointment_data")
            return calendar_service.create_event(appointment_data)

        def send_confirmation(context, **kwargs):
            from ..integrations.services import email_service

            appointment_data = context.get("appointment_data")
            return email_service.send_appointment_reminder(appointment_data)

        workflow.add_step(WorkflowStep("create_event", create_calendar_event))
        workflow.add_step(WorkflowStep("send_confirmation", send_confirmation))

        return workflow

    @staticmethod
    def create_deal_workflow() -> Workflow:
        """Workflow for processing deals"""
        workflow = Workflow("process_deal", "Process and track deals")

        def calculate_deal_score(context, **kwargs):
            from ..analytics.deal_scoring import deal_scorer

            property_data = context.get("property_data")
            strategy = context.get("strategy", "buy_and_hold")
            return deal_scorer.calculate_deal_score(property_data, strategy)

        def sync_to_crm(context, **kwargs):
            from ..integrations.services import crm_integration

            deal_data = context.get("deal_data")
            return crm_integration.sync_deal(deal_data)

        workflow.add_step(WorkflowStep("score_deal", calculate_deal_score))
        workflow.add_step(WorkflowStep("sync_crm", sync_to_crm))

        return workflow


# Global workflow library
workflow_library = WorkflowLibrary()
