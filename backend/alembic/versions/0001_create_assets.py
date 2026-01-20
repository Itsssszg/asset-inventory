"""create assets table

Revision ID: 0001_create_assets
Revises: 
Create Date: 2026-01-15

"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa


revision: str = "0001_create_assets"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "assets",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("asset_tag", sa.String(length=64), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("asset_type", sa.String(length=64), nullable=False),
        sa.Column("status", sa.String(length=64), nullable=False, server_default=sa.text("'active'")),
        sa.Column("location", sa.String(length=255), nullable=True),
        sa.Column("serial_number", sa.String(length=255), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    )
    op.create_index("ix_assets_id", "assets", ["id"])
    op.create_index("ix_assets_asset_tag", "assets", ["asset_tag"], unique=True)
    op.create_index("ix_assets_asset_type", "assets", ["asset_type"])
    op.create_index("ix_assets_status", "assets", ["status"])


def downgrade() -> None:
    op.drop_index("ix_assets_status", table_name="assets")
    op.drop_index("ix_assets_asset_type", table_name="assets")
    op.drop_index("ix_assets_asset_tag", table_name="assets")
    op.drop_index("ix_assets_id", table_name="assets")
    op.drop_table("assets")
