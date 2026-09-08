"""add account recovery

Revision ID: 73bbbfbf37df
Revises: 002bbfc73e52
Create Date: 2026-09-05 23:58:29.153706
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "73bbbfbf37df"
down_revision: Union[str, Sequence[str], None] = "002bbfc73e52"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "account_recoveries",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("purpose", sa.String(length=30), nullable=False),
        sa.Column("identifier", sa.String(length=150), nullable=False),
        sa.Column("otp_hash", sa.String(length=128), nullable=True),
        sa.Column("otp_expires_at", sa.DateTime(), nullable=True),
        sa.Column(
            "otp_attempts",
            sa.Integer(),
            nullable=False,
            server_default="0",
        ),
        sa.Column(
            "last_otp_sent_at",
            sa.DateTime(),
            nullable=True,
        ),
        sa.Column(
            "verified",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
            server_default=sa.true(),
        ),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_account_recoveries_user_id",
        "account_recoveries",
        ["user_id"],
    )


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if "account_recoveries" not in inspector.get_table_names():
        return

    indexes = inspector.get_indexes("account_recoveries")

    if any(
        index["name"] == "ix_account_recoveries_user_id"
        for index in indexes
    ):
        op.drop_index(
            "ix_account_recoveries_user_id",
            table_name="account_recoveries",
        )

    op.drop_table("account_recoveries")
