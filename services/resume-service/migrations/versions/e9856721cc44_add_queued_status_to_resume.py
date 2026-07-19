"""add queued status to resume

Revision ID: e9856721cc44
Revises: 7df3b89109ab
Create Date: 2026-07-19 12:12:30.835596
"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "e9856721cc44"
down_revision: Union[str, Sequence[str], None] = "7df3b89109ab"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        "ALTER TYPE resumestatus ADD VALUE IF NOT EXISTS 'QUEUED';"
    )


def downgrade() -> None:
    # PostgreSQL enum values cannot be removed safely.
    pass
