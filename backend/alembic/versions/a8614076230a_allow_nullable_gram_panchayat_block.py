"""allow nullable gram panchayat block

Revision ID: a8614076230a
Revises: 1a2376d8bf36
Create Date: 2026-08-25 01:53:58.732057

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "a8614076230a"
down_revision: Union[str, Sequence[str], None] = "1a2376d8bf36"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table(
        "gram_panchayats",
        recreate="always",
    ) as batch_op:
        batch_op.alter_column(
            "block_id",
            existing_type=sa.Integer(),
            nullable=True,
        )


def downgrade() -> None:
    with op.batch_alter_table(
        "gram_panchayats",
        recreate="always",
    ) as batch_op:
        batch_op.alter_column(
            "block_id",
            existing_type=sa.Integer(),
            nullable=False,
        )
