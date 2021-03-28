"""empty message

Revision ID: 2cc4a8a73a3d
Revises: eefbce263ba6
Create Date: 2021-03-28 16:35:17.574047

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2cc4a8a73a3d'
down_revision = 'eefbce263ba6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('todolist',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('todos', sa.Column('todolist_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'todos', 'todolist', ['todolist_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'todos', type_='foreignkey')
    op.drop_column('todos', 'todolist_id')
    op.drop_table('todolist')
    # ### end Alembic commands ###
