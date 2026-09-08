from typing import List

from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.dependencies.database import get_db

from app.schemas.government.retirement_schema import (
    RetirementCreate,
    RetirementResponse,
)

from app.services.government.retirement_service import (
    create_retirement_service,
    get_retirements_service,
)

router = APIRouter(
    prefix="/retirements",
    tags=["Retirement"],
)


@router.post(
    "/",
    response_model=RetirementResponse,
    summary="Create New Retirement",
)
def create_new_retirement(
    retirement: RetirementCreate,
    db: Session = Depends(get_db),
):
    return create_retirement_service(
        db,
        retirement,
    )


@router.get(
    "/",
    response_model=List[RetirementResponse],
    summary="Read Retirements",
)
def read_retirements(
    db: Session = Depends(get_db),
):
    return get_retirements_service(db)