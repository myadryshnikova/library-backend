"""add_book_table

Revision ID: c46d566ac06c
Revises: d346c45b75d2
Create Date: 2023-12-14 14:02:04.792674

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c46d566ac06c'
down_revision = 'd346c45b75d2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('books',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=2048), nullable=False),
    sa.Column('author', sa.String(length=2048), nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('bookshelf_id', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['bookshelf_id'], ['bookshelfs.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('books')
    # ### end Alembic commands ###