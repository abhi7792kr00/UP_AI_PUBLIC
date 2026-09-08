from sqlalchemy import ForeignKey
from sqlalchemy import UniqueConstraint

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from core.database.base_model import BaseModel


class BlockTehsil(BaseModel):
    __tablename__ = "block_tehsils"

    block_id: Mapped[int] = mapped_column(
        ForeignKey("blocks.id"),
        nullable=False,
    )

    tehsil_id: Mapped[int] = mapped_column(
        ForeignKey("tehsils.id"),
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint(
            "block_id",
            "tehsil_id",
            name="uq_block_tehsil",
        ),
    )
