"""init

Revision ID: c75a14171e2b
Revises: 88168ff7f1fc
Create Date: 2025-03-31 11:53:04.314136

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c75a14171e2b'
down_revision: Union[str, None] = '88168ff7f1fc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
