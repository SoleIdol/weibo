"""empty message

Revision ID: ae171f124ce1
Revises: 6edd2d496dbf
Create Date: 2020-08-28 08:38:23.857864

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ae171f124ce1'
down_revision = '6edd2d496dbf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('n_fans', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'n_fans')
    # ### end Alembic commands ###
