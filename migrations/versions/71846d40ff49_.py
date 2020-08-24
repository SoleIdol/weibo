"""empty message

Revision ID: 71846d40ff49
Revises: 
Create Date: 2020-08-24 16:07:10.361542

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '71846d40ff49'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=10), nullable=False),
    sa.Column('password', sa.String(length=30), nullable=False),
    sa.Column('head', sa.String(length=128), nullable=True),
    sa.Column('gender', sa.Enum('男', '女', '保密'), nullable=True),
    sa.Column('birthday', sa.Date(), nullable=True),
    sa.Column('city', sa.String(length=20), nullable=True),
    sa.Column('reg_time', sa.Date(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###
