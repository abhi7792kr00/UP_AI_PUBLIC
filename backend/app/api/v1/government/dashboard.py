from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.dependencies.database import get_db

from app.schemas.government.dashboard_schema import (
    DashboardResponse,
)

from app.services.government.dashboard_service import (
    get_dashboard,
)

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get(
    "/",
    response_model=DashboardResponse,
)
def dashboard(
    db: Session = Depends(get_db),
):
    return get_dashboard(
        db,
    )