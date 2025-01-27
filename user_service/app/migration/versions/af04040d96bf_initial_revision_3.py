"""Initial revision 3

Revision ID: af04040d96bf
Revises: d2d4a94782b5
Create Date: 2025-01-27 18:38:08.841272

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'af04040d96bf'
down_revision: Union[str, None] = 'd2d4a94782b5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('companies', 'aba')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('companies', sa.Column('aba', sa.INTEGER(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###