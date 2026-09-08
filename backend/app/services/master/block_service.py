from sqlalchemy.orm import Session

from app.repositories.master.block_repository import (
    block_repository,
)

from app.services.base.base_service import BaseService

from database.models.master.block import Block


class BlockService(
    BaseService
):
    def __init__(self):
        super().__init__(
            block_repository
        )

    def get_by_tehsil(
        self,
        db: Session,
        tehsil_id: int,
    ):
        return self.repository.get_by_tehsil(
            db,
            tehsil_id,
        )

    def get_by_code(
        self,
        db: Session,
        block_code: str,
    ):
        return self.repository.get_by_code(
            db,
            block_code,
        )

    def get_tehsil_ids(
        self,
        db: Session,
        block_id: int,
    ) -> list[int]:
        return self.repository.get_tehsil_ids(
            db,
            block_id,
        )

    def is_valid_for_tehsil(
        self,
        db: Session,
        *,
        block_id: int,
        tehsil_id: int,
    ) -> bool:
        return self.repository.exists_for_tehsil(
            db,
            block_id=block_id,
            tehsil_id=tehsil_id,
        )

    def create_block(
        self,
        db: Session,
        *,
        block_name: str,
        block_code: str,
        tehsil_ids: list[int],
    ):
        existing = self.get_by_code(
            db,
            block_code,
        )

        if existing:
            raise ValueError(
                "Block code already exists."
            )

        tehsils = (
            self.repository.get_tehsils(
                db,
                tehsil_ids,
            )
        )

        unique_ids = sorted(
            set(tehsil_ids)
        )

        if len(tehsils) != len(
            unique_ids
        ):
            raise ValueError(
                "One or more Tehsil IDs are invalid."
            )

        block = Block(
            block_name=block_name,
            block_code=block_code,
        )

        db.add(block)
        db.flush()

        self.repository.replace_tehsil_links(
            db,
            block_id=block.id,
            tehsil_ids=unique_ids,
        )

        db.commit()
        db.refresh(block)

        return block

    def update_block(
        self,
        db: Session,
        *,
        block_id: int,
        block_name: str | None,
        block_code: str | None,
        tehsil_ids: list[int] | None,
        is_active: bool | None,
    ):
        block = self.get_by_id(
            db,
            block_id,
        )

        if block is None:
            raise ValueError(
                "Block not found."
            )

        if (
            block_code is not None
            and block_code != block.block_code
        ):
            existing = self.get_by_code(
                db,
                block_code,
            )

            if (
                existing
                and existing.id != block_id
            ):
                raise ValueError(
                    "Block code already exists."
                )

            block.block_code = block_code

        if block_name is not None:
            block.block_name = block_name

        if is_active is not None:
            block.is_active = is_active

        if tehsil_ids is not None:
            unique_ids = sorted(
                set(tehsil_ids)
            )

            tehsils = (
                self.repository.get_tehsils(
                    db,
                    unique_ids,
                )
            )

            if len(tehsils) != len(
                unique_ids
            ):
                raise ValueError(
                    "One or more Tehsil IDs are invalid."
                )

            self.repository.replace_tehsil_links(
                db,
                block_id=block.id,
                tehsil_ids=unique_ids,
            )

        db.add(block)
        db.commit()
        db.refresh(block)

        return block


block_service = BlockService()
