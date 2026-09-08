from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.dependencies.database import get_db

from app.api.v1.complaint.complaint_request import (
    ComplaintCreateRequest,
)

from app.api.v1.complaint.complaint_response import (
    ComplaintResponse,
)

from app.api.v1.complaint.complaint_timeline_response import (
    ComplaintTimelineResponse,
)

from app.api.v1.complaint.complaint_mapper import (
    ComplaintMapper,
)

from app.bootstrap.complaint import (
    complaint_registration_engine,
)

from app.services.complaint.complaint_service import (
    complaint_service,
)

from app.services.workflow.workflow_history_service import (
    workflow_history_service,
)

from app.api.v1.complaint.complaint_transition_request import (
    ComplaintTransitionRequest,
)

from app.api.v1.complaint.complaint_transition_response import (
    ComplaintTransitionResponse,
)


router = APIRouter(
    prefix="/complaints",
    tags=["Complaints"],
)


# ============================================================
# REGISTER COMPLAINT
# ============================================================

@router.post(
    "",
    response_model=ComplaintResponse,
)
def register_complaint(
    request: ComplaintCreateRequest,
    db: Session = Depends(get_db),
):
    """
    Register a new complaint.
    """

    complaint_request = (
        ComplaintMapper.to_dto(
            request,
        )
    )

    complaint = (
        complaint_registration_engine.register_complaint(
            db=db,
            request=complaint_request,
        )
    )

    return ComplaintMapper.to_response(
        complaint,
    )


# ============================================================
# GET COMPLAINT BY COMPLAINT NUMBER
# ============================================================

@router.get(
    "/{complaint_number}",
    response_model=ComplaintResponse,
)
def get_complaint(
    complaint_number: str,
    db: Session = Depends(get_db),
):
    """
    Get complaint details by complaint number.
    """

    complaint = (
        complaint_service.get_by_complaint_number(
            db=db,
            complaint_number=complaint_number,
        )
    )

    if complaint is None:
        raise HTTPException(
            status_code=404,
            detail="Complaint not found",
        )

    return ComplaintMapper.to_response(
        complaint,
    )


# ============================================================
# GET COMPLAINT TIMELINE
# ============================================================

@router.get(
    "/{complaint_number}/timeline",
    response_model=list[ComplaintTimelineResponse],
)
def get_complaint_timeline(
    complaint_number: str,
    db: Session = Depends(get_db),
):
    """
    Get complete workflow timeline
    of a complaint.
    """

    complaint = (
        complaint_service.get_by_complaint_number(
            db=db,
            complaint_number=complaint_number,
        )
    )

    if complaint is None:
        raise HTTPException(
            status_code=404,
            detail="Complaint not found",
        )

    history = (
        workflow_history_service.get_history(
            db=db,
            reference_number=complaint_number,
        )
    )

    if history is None:
        return []

    return [
        ComplaintTimelineResponse(
            id=item.id,
            workflow_definition_id=item.workflow_definition_id,
            workflow_step_id=item.workflow_step_id,
            reference_number=item.reference_number,
            action=item.action,
            remarks=item.remarks,
            performed_by=item.performed_by,
            created_at=item.created_at,
            updated_at=item.updated_at,
        )
        for item in history
    ]


# ============================================================
# TRANSITION COMPLAINT
# ============================================================

@router.post(
    "/{complaint_number}/transition",
    response_model=ComplaintTransitionResponse,
    summary="Transition Complaint",
    description="Move complaint to another workflow status.",
)
def transition_complaint(
    complaint_number: str,
    request: ComplaintTransitionRequest,
    db: Session = Depends(get_db),
):
    return complaint_service.transition(
        db=db,
        complaint_number=complaint_number,
        to_status_id=request.to_status_id,
        remarks=request.remarks,
        performed_by=request.performed_by,
    )