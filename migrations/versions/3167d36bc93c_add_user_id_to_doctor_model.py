"""Add user_id to Doctor model

Revision ID: 3167d36bc93c
Revises: f2c7cf815d8a
Create Date: 2025-12-05 11:20:42.951017

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3167d36bc93c'
down_revision = 'f2c7cf815d8a'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('doctor', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(
            'fk_doctor_user_id',   # ✅ give it a name
            'user',
            ['user_id'],
            ['id']
        )

    # ### end Alembic commands ###


def downgrade():
    with op.batch_alter_table('doctor', schema=None) as batch_op:
        # Drop foreign key constraint if named
        batch_op.drop_constraint('fk_doctor_user_id', type_='foreignkey')
        # Drop unnamed constraints if Alembic generated them
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='unique')
        # Finally drop the column
        batch_op.drop_column('user_id')


    # ### end Alembic commands ###
