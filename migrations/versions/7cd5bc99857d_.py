"""empty message

Revision ID: 7cd5bc99857d
Revises: 1cfab067f728
Create Date: 2024-03-20 15:04:43.942887

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7cd5bc99857d'
down_revision = '1cfab067f728'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_favorite', schema=None) as batch_op:
        batch_op.drop_constraint('user_favorite_planets_id_fkey', type_='foreignkey')
        batch_op.drop_column('planets_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_favorite', schema=None) as batch_op:
        batch_op.add_column(sa.Column('planets_id', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.create_foreign_key('user_favorite_planets_id_fkey', 'planet', ['planets_id'], ['id'])

    # ### end Alembic commands ###
