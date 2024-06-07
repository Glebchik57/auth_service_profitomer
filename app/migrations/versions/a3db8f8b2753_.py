"""empty message

Revision ID: a3db8f8b2753
Revises: 574167c3eeed
Create Date: 2024-06-02 10:20:17.103449

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a3db8f8b2753'
down_revision: Union[str, None] = '574167c3eeed'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
