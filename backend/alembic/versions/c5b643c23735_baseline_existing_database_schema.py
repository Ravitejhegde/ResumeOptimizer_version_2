"""baseline existing database schema

Revision ID: c5b643c23735
Revises:
Create Date: 2026-08-14
"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "c5b643c23735"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Mark the existing database schema as the baseline."""
    pass


def downgrade() -> None:
    """Baseline migration has no destructive downgrade."""
    pass