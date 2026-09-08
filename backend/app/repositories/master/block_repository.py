from sqlalchemy.orm import Session

from app.repositories.base.base_repository import BaseRepository

from database.models.master.block import Block
from database.models.master.block_tehsil import BlockTehsil
from database.models.master.tehsil import Tehsil


class BlockRepository(
    BaseRepository[Block]
):
    def __init__(self):
        super().__init__(Block)

    def get_by_tehsil(
        self,
        db: Session,
        tehsil_id: int,
    ):
        return (
            db.query(Block)
            .join(
                BlockTehsil,
                BlockTehsil.block_id == Block.id,
            )
            .filter(
                BlockTehsil.tehsil_id == tehsil_id,
                BlockTehsil.is_active.is_(True),
                Block.is_active.is_(True),
            )
            .order_by(
                Block.block_name.asc()
            )
            .all()
        )

    def get_by_code(
        self,
        db: Session,
        block_code: str,
    ):
        return (
            db.query(Block)
            .filter(
                Block.block_code == block_code
            )
            .first()
        )

    def get_tehsil_ids(
        self,
        db: Session,
        block_id: int,
    ) -> list[int]:
        rows = (
            db.query(BlockTehsil.tehsil_id)
            .filter(
                BlockTehsil.block_id == block_id,
                BlockTehsil.is_active.is_(True),
            )
            .order_by(
                BlockTehsil.tehsil_id.asc()
            )
            .all()
        )

        return [
            row[0]
            for row in rows
        ]

    def get_tehsils(
        self,
        db: Session,
        tehsil_ids: list[int],
    ):
        if not tehsil_ids:
            return []

        return (
            db.query(Tehsil)
            .filter(
                Tehsil.id.in_(tehsil_ids),
                Tehsil.is_active.is_(True),
            )
            .all()
        )

    def replace_tehsil_links(
        self,
        db: Session,
        *,
        block_id: int,
        tehsil_ids: list[int],
    ):
        (
            db.query(BlockTehsil)
            .filter(
                BlockTehsil.block_id == block_id
            )
            .delete(
                synchronize_session=False
            )
        )

        unique_ids = sorted(
            set(tehsil_ids)
        )

        for tehsil_id in unique_ids:
            db.add(
                BlockTehsil(
                    block_id=block_id,
                    tehsil_id=tehsil_id,
                    is_active=True,
                )
            )

    def exists_for_tehsil(
        self,
        db: Session,
        *,
        block_id: int,
        tehsil_id: int,
    ) -> bool:
        return (
            db.query(BlockTehsil.id)
            .filter(
                BlockTehsil.block_id == block_id,
                BlockTehsil.tehsil_id == tehsil_id,
                BlockTehsil.is_active.is_(True),
            )
            .first()
            is not None
        )


block_repository = BlockRepository()
