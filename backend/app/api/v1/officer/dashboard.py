from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.dependencies.database import get_db

from app.schemas.officer.dashboard_schema import (
    OfficerDashboardResponse,
)

from app.services.officer.dashboard_service import (
    get_officer_dashboard,
)


router = APIRouter(
    prefix="/officer",
    tags=["Officer Dashboard"],
)


@router.get(
    "/dashboard/{officer_id}",
    response_model=OfficerDashboardResponse,
)
def officer_dashboard(
    officer_id: int,
    db: Session = Depends(get_db),
):

    try:
        return get_officer_dashboard(
            db=db,
            officer_id=officer_id,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )