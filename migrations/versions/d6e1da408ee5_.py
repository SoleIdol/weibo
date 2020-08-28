"""empty message

Revision ID: d6e1da408ee5
Revises: ae171f124ce1
Create Date: 2020-08-28 08:43:09.522161

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd6e1da408ee5'
down_revision = 'ae171f124ce1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('idol',
    sa.Column('idol_id', sa.Integer(), nullable=False),
    sa.Column('fans_id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('idol_id', 'fans_id')
    )
    op.create_table('message',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('fid', sa.Integer(), nullable=True),
    sa.Column('iid', sa.Integer(), nullable=True),
    sa.Column('yid', sa.Integer(), nullable=True),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('up_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('thumb',
    sa.Column('wid', sa.Integer(), nullable=False),
    sa.Column('uid', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('wid', 'uid')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=10), nullable=False),
    sa.Column('password', sa.String(length=128), nullable=False),
    sa.Column('head', sa.String(length=128), nullable=True),
    sa.Column('gender', sa.Enum('男', '女', '保密'), nullable=True),
    sa.Column('n_fans', sa.Integer(), nullable=True),
    sa.Column('birthday', sa.Date(), nullable=True),
    sa.Column('city', sa.String(length=20), nullable=True),
    sa.Column('reg_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('weibo',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uid', sa.Integer(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('filename', sa.String(length=256), nullable=True),
    sa.Column('zan_num', sa.Integer(), nullable=True),
    sa.Column('public', sa.Boolean(), nullable=True),
    sa.Column('cr_time', sa.DateTime(), nullable=True),
    sa.Column('up_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_weibo_uid'), 'weibo', ['uid'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_weibo_uid'), table_name='weibo')
    op.drop_table('weibo')
    op.drop_table('user')
    op.drop_table('thumb')
    op.drop_table('message')
    op.drop_table('idol')
    # ### end Alembic commands ###