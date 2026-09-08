"""
Workflow Bootstrap

Creates all workflow engines.
"""

from app.bootstrap.services import (
    workflow_definition_service,
    workflow_step_service,
    workflow_assignment_service,
    workflow_history_service,
)

from app.engines.workflow.workflow_resolver import (
    WorkflowResolver,
)

from app.engines.workflow.workflow_runtime_engine import (
    WorkflowRuntimeEngine,
)

from app.engines.complaint.assignment_engine import (
    AssignmentEngine,
)

from app.engines.complaint.timeline_engine import (
    TimelineEngine,
)

# ---------------------------------
# Engines
# ---------------------------------

workflow_resolver = (
    WorkflowResolver(
        workflow_definition_service,
        workflow_step_service,
    )
)

assignment_engine = (
    AssignmentEngine(
        workflow_assignment_service,
    )
)

timeline_engine = (
    TimelineEngine(
        workflow_history_service,
    )
)

workflow_runtime_engine = (
    WorkflowRuntimeEngine(
        workflow_resolver,
        assignment_engine,
        timeline_engine,
    )
)

__all__ = [
    "workflow_resolver",
    "assignment_engine",
    "timeline_engine",
    "workflow_runtime_engine",
]