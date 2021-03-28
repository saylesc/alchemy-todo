"""empty message

Revision ID: 600fa681d26c
Revises: 2cc4a8a73a3d
Create Date: 2021-03-28 16:45:33.784130

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '600fa681d26c'
down_revision = '2cc4a8a73a3d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('todos', 'todolist_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('todos', 'todolist_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###
