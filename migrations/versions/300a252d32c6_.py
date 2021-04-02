"""empty message

Revision ID: 300a252d32c6
Revises: 600fa681d26c
Create Date: 2021-04-02 08:30:39.031339

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '300a252d32c6'
down_revision = '600fa681d26c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('todolist', sa.Column('completed', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('todolist', 'completed')
    # ### end Alembic commands ###