from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.dependencies.database import get_db

from app.schemas.government.service_history_schema import (
    ServiceHistoryResponse,
)

from app.services.government.service_history_service import (
    get_service_history,
)

router = APIRouter(
    prefix="/service-history",
    tags=["Service History"],
)


@router.get(
    "/{officer_id}",
    response_model=list[ServiceHistoryResponse],
)
def read_service_history(
    officer_id: int,
    db: Session = Depends(get_db),
):
    return get_service_history(
        db,
        officer_id,
    )