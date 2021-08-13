"""empty message

Revision ID: 721ba9118b88
Revises: e2ef44bbeadd
Create Date: 2021-08-13 15:49:21.080658

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '721ba9118b88'
down_revision = 'e2ef44bbeadd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('options', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['name'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('options', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')

    # ### end Alembic commands ###