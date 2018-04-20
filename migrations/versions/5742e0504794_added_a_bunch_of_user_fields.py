"""added a bunch of user fields

Revision ID: 5742e0504794
Revises: c3a21353da90
Create Date: 2018-04-15 21:52:26.605872

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5742e0504794'
down_revision = 'c3a21353da90'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('activity_level', sa.String(length=2), nullable=True))
    op.add_column('user', sa.Column('city', sa.String(length=40), nullable=True))
    op.add_column('user', sa.Column('country', sa.String(length=40), nullable=True))
    op.add_column('user', sa.Column('date_of_birth', sa.DateTime(), nullable=True))
    op.add_column('user', sa.Column('goal', sa.String(length=2), nullable=True))
    op.add_column('user', sa.Column('height', sa.Integer(), nullable=True))
    op.add_column('user', sa.Column('sex', sa.String(length=1), nullable=True))
    op.add_column('user', sa.Column('weight', sa.Integer(), nullable=True))
    op.add_column('user', sa.Column('workouts_per_week', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'workouts_per_week')
    op.drop_column('user', 'weight')
    op.drop_column('user', 'sex')
    op.drop_column('user', 'height')
    op.drop_column('user', 'goal')
    op.drop_column('user', 'date_of_birth')
    op.drop_column('user', 'country')
    op.drop_column('user', 'city')
    op.drop_column('user', 'activity_level')
    # ### end Alembic commands ###