"""add roles and publication workflow

Revision ID: 004
Revises: 003
Create Date: 2026-04-14
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "004"
down_revision: str | None = "003"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("users", sa.Column("role", sa.String(), nullable=True))
    op.execute("UPDATE users SET role = 'user' WHERE role IS NULL")
    op.alter_column("users", "role", nullable=False)

    op.add_column("recipes", sa.Column("visibility", sa.String(), nullable=True))
    op.add_column("recipes", sa.Column("publication_status", sa.String(), nullable=True))
    op.add_column("recipes", sa.Column("is_admin_recipe", sa.Boolean(), nullable=True))
    op.add_column("recipes", sa.Column("approved_by", sa.Integer(), nullable=True))
    op.add_column("recipes", sa.Column("approved_at", sa.DateTime(), nullable=True))
    op.add_column("recipes", sa.Column("rejection_reason", sa.Text(), nullable=True))
    op.add_column("recipes", sa.Column("original_recipe_id", sa.Integer(), nullable=True))

    op.execute("UPDATE recipes SET visibility = 'private' WHERE visibility IS NULL")
    op.execute("UPDATE recipes SET publication_status = 'draft' WHERE publication_status IS NULL")
    op.execute("UPDATE recipes SET is_admin_recipe = FALSE WHERE is_admin_recipe IS NULL")

    op.alter_column("recipes", "visibility", nullable=False)
    op.alter_column("recipes", "publication_status", nullable=False)
    op.alter_column("recipes", "is_admin_recipe", nullable=False)

    op.create_foreign_key(
        "fk_recipes_approved_by_users",
        "recipes",
        "users",
        ["approved_by"],
        ["id"],
    )
    op.create_foreign_key(
        "fk_recipes_original_recipe_id_recipes",
        "recipes",
        "recipes",
        ["original_recipe_id"],
        ["id"],
    )


def downgrade() -> None:
    op.drop_constraint("fk_recipes_original_recipe_id_recipes", "recipes", type_="foreignkey")
    op.drop_constraint("fk_recipes_approved_by_users", "recipes", type_="foreignkey")
    op.drop_column("recipes", "original_recipe_id")
    op.drop_column("recipes", "rejection_reason")
    op.drop_column("recipes", "approved_at")
    op.drop_column("recipes", "approved_by")
    op.drop_column("recipes", "is_admin_recipe")
    op.drop_column("recipes", "publication_status")
    op.drop_column("recipes", "visibility")
    op.drop_column("users", "role")
