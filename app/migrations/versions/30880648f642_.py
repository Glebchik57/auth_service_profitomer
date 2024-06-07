"""empty message

Revision ID: 30880648f642
Revises: 7a4621146982
Create Date: 2024-06-06 22:45:58.012574

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '30880648f642'
down_revision: Union[str, None] = '7a4621146982'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
