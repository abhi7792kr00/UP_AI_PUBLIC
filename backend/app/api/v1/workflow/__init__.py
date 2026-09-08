from fastapi import APIRouter

from .workflow_definition import router as workflow_definition_router
from .workflow_step import router as workflow_step_router
from .workflow_transition import router as workflow_transition_router
from .workflow_history import router as workflow_history_router
from .workflow_assignment import router as workflow_assignment_router
from .workflow_runtime import router as workflow_runtime_router

router = APIRouter(
    prefix="/workflow",
)

router.include_router(workflow_definition_router)
router.include_router(workflow_step_router)
router.include_router(workflow_transition_router)
router.include_router(workflow_history_router)
router.include_router(workflow_assignment_router)
router.include_router(workflow_runtime_router)