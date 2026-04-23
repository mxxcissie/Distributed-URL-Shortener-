"""drop redundant id index

Revision ID: dbd94075bc5e
Revises: 81e30324ebdc
Create Date: 2026-04-22 22:16:14.895949

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dbd94075bc5e'
down_revision: Union[str, Sequence[str], None] = '81e30324ebdc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    indexes = {index["name"] for index in inspector.get_indexes("urls")}

    if "ix_urls_id" in indexes:
        op.drop_index("ix_urls_id", table_name="urls")


def downgrade() -> None:
    """Downgrade schema."""
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    indexes = {index["name"] for index in inspector.get_indexes("urls")}

    if "ix_urls_id" not in indexes:
        op.create_index("ix_urls_id", "urls", ["id"], unique=False)
