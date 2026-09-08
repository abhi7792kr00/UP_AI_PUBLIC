from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db

from app.schemas.block_schema import (
    BlockCreate,
    BlockUpdate,
    BlockResponse,
)

from app.services.master.block_service import (
    block_service,
)


router = APIRouter(
    prefix="/blocks",
    tags=["Blocks"],
)


def to_response(
    db: Session,
    block,
) -> BlockResponse:
    return BlockResponse(
        id=block.id,
        block_name=block.block_name,
        block_code=block.block_code,
        is_active=block.is_active,
        created_at=block.created_at,
        updated_at=block.updated_at,
        tehsil_ids=block_service.get_tehsil_ids(
            db,
            block.id,
        ),
    )


@router.get(
    "/",
    response_model=List[BlockResponse],
)
def read_blocks(
    db: Session = Depends(get_db),
):
    blocks = block_service.get_all(db)

    return [
        to_response(db, block)
        for block in blocks
    ]


@router.get(
    "/tehsil/{tehsil_id}",
    response_model=List[BlockResponse],
)
def read_blocks_by_tehsil(
    tehsil_id: int,
    db: Session = Depends(get_db),
):
    blocks = block_service.get_by_tehsil(
        db,
        tehsil_id,
    )

    return [
        to_response(db, block)
        for block in blocks
    ]


@router.get(
    "/{block_id}",
    response_model=BlockResponse,
)
def read_block(
    block_id: int,
    db: Session = Depends(get_db),
):
    block = block_service.get_by_id(
        db,
        block_id,
    )

    if not block:
        raise HTTPException(
            status_code=404,
            detail="Block not found",
        )

    return to_response(
        db,
        block,
    )


@router.post(
    "/",
    response_model=BlockResponse,
)
def create_block(
    block: BlockCreate,
    db: Session = Depends(get_db),
):
    try:
        obj = block_service.create_block(
            db,
            block_name=block.block_name,
            block_code=block.block_code,
            tehsil_ids=block.tehsil_ids,
        )

        return to_response(
            db,
            obj,
        )

    except ValueError as exc:
        db.rollback()

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


@router.put(
    "/{block_id}",
    response_model=BlockResponse,
)
def update_block(
    block_id: int,
    block: BlockUpdate,
    db: Session = Depends(get_db),
):
    try:
        obj = block_service.update_block(
            db,
            block_id=block_id,
            block_name=block.block_name,
            block_code=block.block_code,
            tehsil_ids=block.tehsil_ids,
            is_active=block.is_active,
        )

        return to_response(
            db,
            obj,
        )

    except ValueError as exc:
        db.rollback()

        status_code = (
            404
            if str(exc) == "Block not found."
            else 400
        )

        raise HTTPException(
            status_code=status_code,
            detail=str(exc),
        )


@router.delete(
    "/{block_id}",
)
def delete_block(
    block_id: int,
    db: Session = Depends(get_db),
):
    obj = block_service.get_by_id(
        db,
        block_id,
    )

    if not obj:
        raise HTTPException(
            status_code=404,
            detail="Block not found",
        )

    block_service.delete(
        db,
        obj,
    )

    return {
        "message": "Block deleted successfully"
    }
