from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.dependencies.database import get_db

from app.schemas.master.municipal_body_schema import (
    MunicipalBodyCreate,
    MunicipalBodyUpdate,
    MunicipalBodyResponse,
)

from app.services.master.municipal_body_service import (
    municipal_body_service,
)

from database.models.master.municipal_body import (
    MunicipalBody,
)

router = APIRouter(
    prefix="/municipal-bodies",
    tags=["Municipal Bodies"],
)


@router.get(
    "/",
    response_model=list[MunicipalBodyResponse],
)
def read_municipal_bodies(
    db: Session = Depends(get_db),
):
    return municipal_body_service.get_all(db)


@router.get(
    "/{body_id}",
    response_model=MunicipalBodyResponse,
)
def read_municipal_body(
    body_id: int,
    db: Session = Depends(get_db),
):
    body = municipal_body_service.get_by_id(
        db,
        body_id,
    )

    if not body:
        raise HTTPException(
            status_code=404,
            detail="Municipal Body not found",
        )

    return body


@router.post(
    "/",
    response_model=MunicipalBodyResponse,
)
def create_municipal_body(
    body: MunicipalBodyCreate,
    db: Session = Depends(get_db),
):
    body_obj = MunicipalBody(
        **body.model_dump()
    )

    return municipal_body_service.create(
        db,
        body_obj,
    )


@router.put(
    "/{body_id}",
    response_model=MunicipalBodyResponse,
)
def update_municipal_body(
    body_id: int,
    body: MunicipalBodyUpdate,
    db: Session = Depends(get_db),
):
    db_obj = municipal_body_service.get_by_id(
        db,
        body_id,
    )

    if not db_obj:
        raise HTTPException(
            status_code=404,
            detail="Municipal Body not found",
        )

    update_data = body.model_dump(
        exclude_unset=True,
    )

    for key, value in update_data.items():
        setattr(
            db_obj,
            key,
            value,
        )

    return municipal_body_service.update(
        db,
        db_obj,
    )


@router.delete(
    "/{body_id}",
)
def delete_municipal_body(
    body_id: int,
    db: Session = Depends(get_db),
):
    db_obj = municipal_body_service.get_by_id(
        db,
        body_id,
    )

    if not db_obj:
        raise HTTPException(
            status_code=404,
            detail="Municipal Body not found",
        )

    municipal_body_service.delete(
        db,
        db_obj,
    )

    return {
        "message": "Municipal Body deleted successfully"
    }