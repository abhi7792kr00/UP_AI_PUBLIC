from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies.database import get_db

from app.schemas.government.posting_schema import (
    PostingCreate,
    PostingUpdate,
    PostingResponse,
)

from app.services.government.posting_service import (
    get_postings,
    get_posting,
    create_posting,
    update_posting,
    delete_posting,
)

router = APIRouter(
    prefix="/postings",
    tags=["Posting"],
)


@router.get(
    "/",
    response_model=list[PostingResponse],
)
def read_postings(
    db: Session = Depends(get_db),
):
    return get_postings(db)


@router.get(
    "/{posting_id}",
    response_model=PostingResponse,
)
def read_posting(
    posting_id: int,
    db: Session = Depends(get_db),
):
    posting = get_posting(
        db,
        posting_id,
    )

    if not posting:
        raise HTTPException(
            status_code=404,
            detail="Posting not found",
        )

    return posting


@router.post(
    "/",
    response_model=PostingResponse,
)
def create_new_posting(
    posting: PostingCreate,
    db: Session = Depends(get_db),
):
    return create_posting(
        db,
        posting,
    )


@router.put(
    "/{posting_id}",
    response_model=PostingResponse,
)
def update_existing_posting(
    posting_id: int,
    posting: PostingUpdate,
    db: Session = Depends(get_db),
):
    updated = update_posting(
        db,
        posting_id,
        posting,
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Posting not found",
        )

    return updated


@router.delete(
    "/{posting_id}",
)
def delete_existing_posting(
    posting_id: int,
    db: Session = Depends(get_db),
):
    deleted = delete_posting(
        db,
        posting_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Posting not found",
        )

    return {
        "message": "Posting deleted successfully"
    }