"""expand municipal body types and remove body name uniqueness

Revision ID: 002bbfc73e52
Revises: 17291e5867ea
Create Date: 2026-08-27
"""

from typing import Sequence, Union

from alembic import op


revision: str = "002bbfc73e52"
down_revision: Union[str, Sequence[str], None] = "17291e5867ea"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("DROP TABLE municipal_bodies")

    op.execute("""
        CREATE TABLE municipal_bodies (
            body_name VARCHAR(150) NOT NULL,
            body_code VARCHAR(20) NOT NULL,
            body_type VARCHAR(30) NOT NULL,
            district_id INTEGER NOT NULL,
            headquarters VARCHAR(200),
            id INTEGER NOT NULL,
            created_at DATETIME NOT NULL,
            updated_at DATETIME NOT NULL,
            is_active BOOLEAN NOT NULL,
            PRIMARY KEY (id),
            FOREIGN KEY(district_id)
                REFERENCES districts (id),
            UNIQUE (body_code)
        )
    """)

    op.execute("""
        CREATE INDEX ix_municipal_bodies_id
        ON municipal_bodies (id)
    """)


def downgrade() -> None:
    op.execute("DROP TABLE municipal_bodies")

    op.execute("""
        CREATE TABLE municipal_bodies (
            body_name VARCHAR(150) NOT NULL,
            body_code VARCHAR(20) NOT NULL,
            body_type VARCHAR(21) NOT NULL,
            district_id INTEGER NOT NULL,
            headquarters VARCHAR(200),
            id INTEGER NOT NULL,
            created_at DATETIME NOT NULL,
            updated_at DATETIME NOT NULL,
            is_active BOOLEAN NOT NULL,
            PRIMARY KEY (id),
            FOREIGN KEY(district_id)
                REFERENCES districts (id),
            UNIQUE (body_code),
            UNIQUE (body_name)
        )
    """)

    op.execute("""
        CREATE INDEX ix_municipal_bodies_id
        ON municipal_bodies (id)
    """)
