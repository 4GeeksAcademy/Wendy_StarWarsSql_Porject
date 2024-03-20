"""empty message

Revision ID: aff6a75c3e4d
Revises: 7cd5bc99857d
Create Date: 2024-03-20 15:16:37.477674

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aff6a75c3e4d'
down_revision = '7cd5bc99857d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_favorite', schema=None) as batch_op:
        batch_op.drop_constraint('user_favorite_people_id_fkey', type_='foreignkey')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_favorite', schema=None) as batch_op:
        batch_op.create_foreign_key('user_favorite_people_id_fkey', 'people', ['people_id'], ['id'])

    # ### end Alembic commands ###
