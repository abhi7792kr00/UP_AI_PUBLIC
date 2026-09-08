"""allow nullable village gram panchayat

Revision ID: 8f80a8334a33
Revises: a8614076230a
Create Date: 2026-08-26 23:06:41.855602

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "8f80a8334a33"
down_revision: Union[str, Sequence[str], None] = "a8614076230a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table(
        "villages",
        recreate="always",
    ) as batch_op:
        batch_op.alter_column(
            "gram_panchayat_id",
            existing_type=sa.INTEGER(),
            nullable=True,
        )


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table(
        "villages",
        recreate="always",
    ) as batch_op:
        batch_op.alter_column(
            "gram_panchayat_id",
            existing_type=sa.INTEGER(),
            nullable=False,
        )
