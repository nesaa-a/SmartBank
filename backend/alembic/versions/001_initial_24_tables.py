"""initial 24 tables

Revision ID: 001_initial_24_tables
Revises:
Create Date: 2026-05-18

"""

from typing import Sequence, Union

from alembic import op

import app.models  # noqa: F401 - register metadata
from app.models import Base

revision: str = "001_initial_24_tables"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    Base.metadata.create_all(bind)


def downgrade() -> None:
    bind = op.get_bind()
    Base.metadata.drop_all(bind)
