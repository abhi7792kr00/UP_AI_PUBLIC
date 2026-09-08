from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.dependencies.database import get_db

from app.schemas.reference import (
    ReferenceSequenceCreate,
    ReferenceSequenceUpdate,
    ReferenceSequenceResponse,
)

from app.services.reference.reference_sequence_service import (
    reference_sequence_service,
)

from app.services.reference.reference_format_service import (
    reference_format_service,
)

from app.repositories.reference.reference_sequence_repository import (
    reference_sequence_repository,
)

from database.models.reference.reference_sequence import (
    ReferenceSequence,
)


router = APIRouter(
    prefix="/reference-sequences",
    tags=["Reference Sequence"],
)


@router.get(
    "/",
    response_model=List[ReferenceSequenceResponse],
)
def read_reference_sequences(
    db: Session = Depends(get_db),
):
    return reference_sequence_service.get_all(db)


@router.get(
    "/{sequence_id}",
    response_model=ReferenceSequenceResponse,
)
def read_reference_sequence(
    sequence_id: int,
    db: Session = Depends(get_db),
):
    obj = reference_sequence_service.get_by_id(
        db,
        sequence_id,
    )

    if obj is None:
        raise HTTPException(
            status_code=404,
            detail="Reference sequence not found",
        )

    return obj


@router.post(
    "/",
    response_model=ReferenceSequenceResponse,
)
def create_reference_sequence(
    sequence: ReferenceSequenceCreate,
    db: Session = Depends(get_db),
):
    if not reference_format_service.exists(
        db,
        sequence.reference_format_id,
    ):
        raise HTTPException(
            status_code=404,
            detail="Reference format not found",
        )

    exists = (
        reference_sequence_repository
        .get_by_format_and_period(
            db=db,
            reference_format_id=sequence.reference_format_id,
            sequence_period=sequence.sequence_period,
            period_value=sequence.period_value,
        )
    )

    if exists:
        raise HTTPException(
            status_code=400,
            detail="Sequence already exists",
        )

    obj = ReferenceSequence(
        **sequence.model_dump()
    )

    return reference_sequence_service.create(
        db,
        obj,
    )


@router.put(
    "/{sequence_id}",
    response_model=ReferenceSequenceResponse,
)
def update_reference_sequence(
    sequence_id: int,
    sequence: ReferenceSequenceUpdate,
    db: Session = Depends(get_db),
):
    obj = reference_sequence_service.get_by_id(
        db,
        sequence_id,
    )

    if obj is None:
        raise HTTPException(
            status_code=404,
            detail="Reference sequence not found",
        )

    update_data = sequence.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(
            obj,
            key,
            value,
        )

    return reference_sequence_service.update(
        db,
        obj,
    )


@router.delete(
    "/{sequence_id}",
)
def delete_reference_sequence(
    sequence_id: int,
    db: Session = Depends(get_db),
):
    obj = reference_sequence_service.get_by_id(
        db,
        sequence_id,
    )

    if obj is None:
        raise HTTPException(
            status_code=404,
            detail="Reference sequence not found",
        )

    reference_sequence_service.delete(
        db,
        obj,
    )

    return {
        "message": "Reference sequence deleted successfully"
    }