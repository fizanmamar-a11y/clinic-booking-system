"""Add Doctor model and doctor_id to Appointment

Revision ID: f2c7cf815d8a
Revises: 3d27420b0d73
Create Date: 2025-12-01 11:03:39.319731

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f2c7cf815d8a'
down_revision = '3d27420b0d73'
branch_labels = None
depends_on = None


def upgrade():
    # Create doctor table
    op.create_table(
        'doctor',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=150), nullable=False),
        sa.Column('specialty', sa.String(length=150), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # Add doctor_id column and foreign key to appointment
    with op.batch_alter_table('appointment', schema=None) as batch_op:
        batch_op.add_column(sa.Column('doctor_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key(
            'fk_appointment_doctor_id',   # explicit name
            'doctor',                     # referent table
            ['doctor_id'],                # local column
            ['id']                        # remote column
        )


def downgrade():
    # Remove doctor_id column and foreign key from appointment
    with op.batch_alter_table('appointment', schema=None) as batch_op:
        batch_op.drop_constraint('fk_appointment_doctor_id', type_='foreignkey')
        batch_op.drop_column('doctor_id')

    # Drop doctor table
    op.drop_table('doctor')
