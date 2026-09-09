"""add complaint subcategory and mapping

Revision ID: 979ece5bf9e8
Revises: 40a0264405ac
Create Date: 2026-08-01 14:57:16.120129

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "979ece5bf9e8"
down_revision: Union[str, Sequence[str], None] = "40a0264405ac"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    print("979 STEP 1: creating complaint_subcategories")

    op.create_table(
        "complaint_subcategories",
        sa.Column("category_id", sa.Integer(), nullable=False),
        sa.Column("subcategory_name", sa.String(length=150), nullable=False),
        sa.Column("subcategory_code", sa.String(length=50), nullable=False),
        sa.Column("description", sa.String(length=300), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ["category_id"],
            ["complaint_categories.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("subcategory_code"),
    )

    op.create_index(
        op.f("ix_complaint_subcategories_id"),
        "complaint_subcategories",
        ["id"],
        unique=False,
    )

    print("979 STEP 1 OK")
    print("979 STEP 2: creating complaint_subcategory_mappings")

    op.create_table(
        "complaint_subcategory_mappings",
        sa.Column("subcategory_id", sa.Integer(), nullable=False),
        sa.Column("administrative_level_id", sa.Integer(), nullable=False),
        sa.Column("department_id", sa.Integer(), nullable=False),
        sa.Column("office_id", sa.Integer(), nullable=False),
        sa.Column("designation_id", sa.Integer(), nullable=False),
        sa.Column("priority_id", sa.Integer(), nullable=False),
        sa.Column("sla_days", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ["administrative_level_id"],
            ["administrative_levels.id"],
        ),
        sa.ForeignKeyConstraint(
            ["department_id"],
            ["departments.id"],
        ),
        sa.ForeignKeyConstraint(
            ["designation_id"],
            ["designations.id"],
        ),
        sa.ForeignKeyConstraint(
            ["office_id"],
            ["offices.id"],
        ),
        sa.ForeignKeyConstraint(
            ["priority_id"],
            ["complaint_priorities.id"],
        ),
        sa.ForeignKeyConstraint(
            ["subcategory_id"],
            ["complaint_subcategories.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        op.f("ix_complaint_subcategory_mappings_id"),
        "complaint_subcategory_mappings",
        ["id"],
        unique=False,
    )

    print("979 STEP 2 OK")
    print("979 STEP 3: adding complaints.subcategory_id")

    op.add_column(
        "complaints",
        sa.Column(
            "subcategory_id",
            sa.Integer(),
            nullable=False,
        ),
    )

    print("979 STEP 3 OK")
    print("979 STEP 4: creating complaint foreign key")

    op.create_foreign_key(
        "fk_complaints_subcategory_id",
        "complaints",
        "complaint_subcategories",
        ["subcategory_id"],
        ["id"],
    )

    print("979 STEP 4 OK")
    print("979 MIGRATION COMPLETE")


def downgrade() -> None:
    """Downgrade schema."""

    print("979 DOWNGRADE: dropping complaint foreign key")

    op.drop_constraint(
        "fk_complaints_subcategory_id",
        "complaints",
        type_="foreignkey",
    )

    op.drop_column(
        "complaints",
        "subcategory_id",
    )

    op.drop_index(
        op.f("ix_complaint_subcategory_mappings_id"),
        table_name="complaint_subcategory_mappings",
    )

    op.drop_table("complaint_subcategory_mappings")

    op.drop_index(
        op.f("ix_complaint_subcategories_id"),
        table_name="complaint_subcategories",
    )

    op.drop_table("complaint_subcategories")

    print("979 DOWNGRADE COMPLETE")
