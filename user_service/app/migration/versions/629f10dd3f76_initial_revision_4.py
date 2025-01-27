"""Initial revision 4

Revision ID: 629f10dd3f76
Revises: af04040d96bf
Create Date: 2025-01-27 20:28:04.888927

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '629f10dd3f76'
down_revision: Union[str, None] = 'af04040d96bf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_invitations_code', table_name='invitations')
    op.drop_index('ix_invitations_id', table_name='invitations')
    op.drop_table('invitations')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('invitations',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('code', sa.VARCHAR(length=36), autoincrement=False, nullable=False),
    sa.Column('company_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('used_by', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['companies.id'], name='invitations_company_id_fkey'),
    sa.ForeignKeyConstraint(['used_by'], ['users.id'], name='invitations_used_by_fkey'),
    sa.PrimaryKeyConstraint('id', name='invitations_pkey')
    )
    op.create_index('ix_invitations_id', 'invitations', ['id'], unique=False)
    op.create_index('ix_invitations_code', 'invitations', ['code'], unique=True)
    # ### end Alembic commands ###