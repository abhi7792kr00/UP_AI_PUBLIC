"""add district relation to blocks

Revision ID: 17291e5867ea
Revises: 8f80a8334a33
Create Date: 2026-08-26 23:54:51.229619

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "17291e5867ea"
down_revision: Union[str, Sequence[str], None] = "8f80a8334a33"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table(
        "blocks",
        recreate="always",
    ) as batch_op:
        batch_op.add_column(
            sa.Column(
                "district_id",
                sa.Integer(),
                nullable=True,
            )
        )

        batch_op.create_foreign_key(
            "fk_blocks_district_id",
            "districts",
            ["district_id"],
            ["id"],
        )

    # Existing test block must remain valid.
    op.execute(
        sa.text(
            """
            UPDATE blocks
            SET district_id = (
                SELECT id
                FROM districts
                WHERE district_code = 'GHAZIPUR'
            )
            WHERE block_code = 'SAIDPUR-BLOCK'
              AND district_id IS NULL
            """
        )
    )

    with op.batch_alter_table(
        "blocks",
        recreate="always",
    ) as batch_op:
        batch_op.alter_column(
            "district_id",
            existing_type=sa.Integer(),
            nullable=False,
        )


def downgrade() -> None:
    with op.batch_alter_table(
        "blocks",
        recreate="always",
    ) as batch_op:
        batch_op.drop_constraint(
            "fk_blocks_district_id",
            type_="foreignkey",
        )
        batch_op.drop_column("district_id")
