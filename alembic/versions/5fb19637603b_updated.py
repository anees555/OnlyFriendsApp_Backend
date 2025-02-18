"""updated

Revision ID: 5fb19637603b
Revises: a17024932f95
Create Date: 2025-02-18 15:40:45.094192

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5fb19637603b'
down_revision: Union[str, None] = 'a17024932f95'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_interest_association', sa.Column('user_id', sa.Integer(), nullable=True))
    op.drop_constraint('user_interest_association_profile_id_fkey', 'user_interest_association', type_='foreignkey')
    op.create_foreign_key(None, 'user_interest_association', 'users', ['user_id'], ['id'])
    op.drop_column('user_interest_association', 'profile_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_interest_association', sa.Column('profile_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'user_interest_association', type_='foreignkey')
    op.create_foreign_key('user_interest_association_profile_id_fkey', 'user_interest_association', 'users', ['profile_id'], ['id'])
    op.drop_column('user_interest_association', 'user_id')
    # ### end Alembic commands ###
