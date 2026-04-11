"""add_recipe_extended_fields

Revision ID: 003
Revises: 002
Create Date: 2026-04-10

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "003"
down_revision: str | None = "002"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("recipes", sa.Column("steps", sa.Text(), nullable=True))
    op.add_column("recipes", sa.Column("tags", sa.Text(), nullable=True))
    op.add_column("recipes", sa.Column("photos", sa.Text(), nullable=True))
    op.add_column("recipes", sa.Column("prep_time", sa.Integer(), nullable=True))
    op.add_column("recipes", sa.Column("cook_time", sa.Integer(), nullable=True))
    op.add_column("recipes", sa.Column("servings", sa.Integer(), nullable=True))
    op.add_column("recipes", sa.Column("difficulty", sa.String(), nullable=True))
    op.add_column("recipes", sa.Column("cuisine", sa.String(), nullable=True))
    op.add_column("recipes", sa.Column("notes", sa.Text(), nullable=True))
    op.add_column(
        "recipes", sa.Column("updated_at", sa.DateTime(), nullable=True)
    )


def downgrade() -> None:
    op.drop_column("recipes", "updated_at")
    op.drop_column("recipes", "notes")
    op.drop_column("recipes", "cuisine")
    op.drop_column("recipes", "difficulty")
    op.drop_column("recipes", "servings")
    op.drop_column("recipes", "cook_time")
    op.drop_column("recipes", "prep_time")
    op.drop_column("recipes", "photos")
    op.drop_column("recipes", "tags")
    op.drop_column("recipes", "steps")
