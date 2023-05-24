"""empty message

Revision ID: 986b9bb30df7
Revises: c6a01c76a9bc
Create Date: 2023-05-18 00:07:47.964492

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '986b9bb30df7'
down_revision = 'c6a01c76a9bc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('project', schema=None) as batch_op:
        batch_op.drop_constraint('project_version_key', type_='unique')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('project', schema=None) as batch_op:
        batch_op.create_unique_constraint('project_version_key', ['version'])

    # ### end Alembic commands ###