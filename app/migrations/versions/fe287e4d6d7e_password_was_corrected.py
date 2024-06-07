"""password was corrected

Revision ID: fe287e4d6d7e
Revises: 1a647631d55e
Create Date: 2024-06-06 23:07:53.255237

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fe287e4d6d7e'
down_revision: Union[str, None] = '1a647631d55e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'password',
               existing_type=sa.VARCHAR(length=64),
               type_=sa.String(length=200),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'password',
               existing_type=sa.String(length=200),
               type_=sa.VARCHAR(length=64),
               existing_nullable=False)
    # ### end Alembic commands ###
