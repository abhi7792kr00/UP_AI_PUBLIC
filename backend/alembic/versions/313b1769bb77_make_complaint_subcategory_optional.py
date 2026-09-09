"""make complaint subcategory optional

Revision ID: 313b1769bb77
Revises: 0f442a68dc2d
Create Date: 2026-08-14 14:52:26.398715

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '313b1769bb77'
down_revision: Union[str, Sequence[str], None] = '0f442a68dc2d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "complaints",
        "subcategory_id",
        existing_type=sa.INTEGER(),
        nullable=True,
    )

    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "officer_id",
                sa.Integer(),
                nullable=True,
            )
        )

        batch_op.create_foreign_key(
            "fk_users_officer_id",
            "officers",
            ["officer_id"],
            ["id"],
        )   # ### end Alembic commands ###


def downgrade() -> None:
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.drop_constraint(
            "fk_users_officer_id",
            type_="foreignkey",
        )

        batch_op.drop_column(
            "officer_id"
        )

    with op.batch_alter_table("complaints", schema=None) as batch_op:
        batch_op.drop_constraint(
            "fk_complaints_subcategory_id",
            type_="foreignkey",
        )

        batch_op.alter_column(
            "subcategory_id",
            existing_type=sa.INTEGER(),
            nullable=False,
        )