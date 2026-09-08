from typing import List

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from sqlalchemy.orm import Session

from app.dependencies import get_db

from app.schemas.gram_panchayat_schema import (
    GramPanchayatCreate,
    GramPanchayatUpdate,
    GramPanchayatResponse,
)

from app.services.master.gram_panchayat_service import (
    gram_panchayat_service,
)


router = APIRouter(
    prefix="/gram-panchayats",
    tags=["Gram Panchayats"],
)


@router.get(
    "/",
    response_model=List[GramPanchayatResponse],
)
def read_gram_panchayats(
    db: Session = Depends(get_db),
):
    return gram_panchayat_service.get_all(db)


# --------------------------------------------------
# Block → Gram Panchayats
# IMPORTANT: must come before /{gram_panchayat_id}
# --------------------------------------------------

@router.get(
    "/block/{block_id}",
    response_model=List[GramPanchayatResponse],
)
def read_gram_panchayats_by_block(
    block_id: int,
    db: Session = Depends(get_db),
):
    return gram_panchayat_service.get_by_block(
        db,
        block_id,
    )


@router.get(
    "/{gram_panchayat_id}",
    response_model=GramPanchayatResponse,
)
def read_gram_panchayat(
    gram_panchayat_id: int,
    db: Session = Depends(get_db),
):
    obj = gram_panchayat_service.get_by_id(
        db,
        gram_panchayat_id,
    )

    if not obj:
        raise HTTPException(
            status_code=404,
            detail="Gram Panchayat not found",
        )

    return obj


@router.post(
    "/",
    response_model=GramPanchayatResponse,
)
def create_gram_panchayat(
    gram_panchayat: GramPanchayatCreate,
    db: Session = Depends(get_db),
):
    return gram_panchayat_service.create(
        db,
        gram_panchayat,
    )


@router.put(
    "/{gram_panchayat_id}",
    response_model=GramPanchayatResponse,
)
def update_gram_panchayat(
    gram_panchayat_id: int,
    gram_panchayat: GramPanchayatUpdate,
    db: Session = Depends(get_db),
):
    obj = gram_panchayat_service.update(
        db,
        gram_panchayat_id,
        gram_panchayat,
    )

    if not obj:
        raise HTTPException(
            status_code=404,
            detail="Gram Panchayat not found",
        )

    return obj


@router.delete(
    "/{gram_panchayat_id}",
)
def delete_gram_panchayat(
    gram_panchayat_id: int,
    db: Session = Depends(get_db),
):
    obj = gram_panchayat_service.delete(
        db,
        gram_panchayat_id,
    )

    if not obj:
        raise HTTPException(
            status_code=404,
            detail="Gram Panchayat not found",
        )

    return {
        "message": "Gram Panchayat deleted successfully"
    }
