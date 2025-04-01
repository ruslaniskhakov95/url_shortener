"""init

Revision ID: 0fbcce075186
Revises: c75a14171e2b
Create Date: 2025-03-31 12:36:55.809953

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0fbcce075186'
down_revision: Union[str, None] = 'c75a14171e2b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
