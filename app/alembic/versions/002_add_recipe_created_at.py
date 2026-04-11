"""Add created_at to recipes

Revision ID: 002
Revises: 001
Create Date: 2026-04-10

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "002"
down_revision: str | None = "001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "recipes",
        sa.Column("created_at", sa.DateTime(), nullable=True),
    )
    op.execute(
        "UPDATE recipes SET created_at = CURRENT_TIMESTAMP WHERE created_at IS NULL"
    )


def downgrade() -> None:
    op.drop_column("recipes", "created_at")
