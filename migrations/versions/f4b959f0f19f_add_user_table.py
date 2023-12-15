"""add-user-table

Revision ID: f4b959f0f19f
Revises: 
Create Date: 2023-12-14 13:42:25.800379

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f4b959f0f19f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('login', sa.String(length=80), nullable=False),
    sa.Column('hashed_password', sa.String(length=64), nullable=False),
    sa.Column('password_salt', sa.String(length=64), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('login'),
    sa.UniqueConstraint('password_salt')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###
