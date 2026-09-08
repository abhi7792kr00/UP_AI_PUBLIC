"""normalize block tehsil relationship

Revision ID: 1a2376d8bf36
Revises: d26ecc4387d3
Create Date: 2026-08-25 01:27:20.719839

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "1a2376d8bf36"
down_revision: Union[str, Sequence[str], None] = "d26ecc4387d3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()

    # ---------------------------------------------------------
    # 1. Create association table.
    # ---------------------------------------------------------

    op.create_table(
        "block_tehsils",
        sa.Column(
            "block_id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "tehsil_id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            nullable=False,
        ),
        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["block_id"],
            ["blocks.id"],
        ),
        sa.ForeignKeyConstraint(
            ["tehsil_id"],
            ["tehsils.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "block_id",
            "tehsil_id",
            name="uq_block_tehsil",
        ),
    )

    op.create_index(
        "ix_block_tehsils_id",
        "block_tehsils",
        ["id"],
        unique=False,
    )

    # ---------------------------------------------------------
    # 2. Preserve existing Block -> Tehsil relations.
    # ---------------------------------------------------------
    #
    # Current DB has blocks.tehsil_id.
    # Copy every valid existing relation to block_tehsils.
    #
    # The SQL uses SQLite's datetime('now') because the current
    # BaseModel timestamps are database-compatible datetime
    # values and this migration must also work on SQLite.
    # ---------------------------------------------------------

    result = bind.execute(
        sa.text(
            """
            INSERT INTO block_tehsils (
                block_id,
                tehsil_id,
                created_at,
                updated_at,
                is_active
            )
            SELECT
                id,
                tehsil_id,
                CURRENT_TIMESTAMP,
                CURRENT_TIMESTAMP,
                is_active
            FROM blocks
            WHERE tehsil_id IS NOT NULL
            """
        )
    )

    print(
        "Preserved Block -> Tehsil relations:",
        result.rowcount,
    )

    # ---------------------------------------------------------
    # 3. Remove old blocks.tehsil_id.
    #
    # SQLite requires batch_alter_table for this.
    # ---------------------------------------------------------

    with op.batch_alter_table(
        "blocks",
        recreate="always",
    ) as batch_op:
        batch_op.drop_column("tehsil_id")


def downgrade() -> None:
    bind = op.get_bind()

    # ---------------------------------------------------------
    # 1. Recreate old blocks.tehsil_id.
    # ---------------------------------------------------------

    with op.batch_alter_table(
        "blocks",
        recreate="always",
    ) as batch_op:
        batch_op.add_column(
            sa.Column(
                "tehsil_id",
                sa.Integer(),
                nullable=True,
            )
        )

    # ---------------------------------------------------------
    # 2. Restore one relation per block.
    #
    # Old schema supports only ONE tehsil per block.
    # For blocks having multiple relations, we choose the
    # lowest association id deterministically.
    # ---------------------------------------------------------

    bind.execute(
        sa.text(
            """
            UPDATE blocks
            SET tehsil_id = (
                SELECT bt.tehsil_id
                FROM block_tehsils bt
                WHERE bt.block_id = blocks.id
                ORDER BY bt.id
                LIMIT 1
            )
            WHERE EXISTS (
                SELECT 1
                FROM block_tehsils bt
                WHERE bt.block_id = blocks.id
            )
            """
        )
    )

    # SQLite requires NOT NULL to be recreated through batch mode.
    # Existing blocks should all have at least one relation in the
    # intended production state.
    with op.batch_alter_table(
        "blocks",
        recreate="always",
    ) as batch_op:

        batch_op.alter_column(
            "tehsil_id",
            existing_type=sa.Integer(),
            nullable=False,
        )

        batch_op.create_foreign_key(
            "fk_blocks_tehsil_id",
            "tehsils",
            ["tehsil_id"],
            ["id"],
        )

    # ---------------------------------------------------------
    # 3. Remove association table.
    # ---------------------------------------------------------

    op.drop_index(
        "ix_block_tehsils_id",
        table_name="block_tehsils",
    )

    op.drop_table("block_tehsils")
