from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.dependencies.current_user import get_current_user

from database.models.auth.user import User

from app.api.v1.officer.officer_dashboard_response import (
    OfficerDashboardResponse,
)

from app.services.officer.dashboard_service import (
    get_officer_dashboard,
)


router = APIRouter(
    prefix="/officer",
    tags=["Officer"],
)


@router.get(
    "/dashboard",
    response_model=OfficerDashboardResponse,
    summary="Get Officer Dashboard",
    description="Get dashboard data for the logged-in officer.",
)
def get_officer_dashboard_api(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    if current_user.officer_id is None:
        raise HTTPException(
            status_code=403,
            detail="User is not linked to an officer.",
        )

    try:
        return get_officer_dashboard(
            db=db,
            officer_id=current_user.officer_id,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )