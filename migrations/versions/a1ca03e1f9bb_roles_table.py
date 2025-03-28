"""Roles table

Revision ID: a1ca03e1f9bb
Revises: e0ecf07c8ca8
Create Date: 2025-03-23 23:12:04.640761

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a1ca03e1f9bb'
down_revision = 'e0ecf07c8ca8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Cars',
    sa.Column('carid', sa.Integer(), nullable=False),
    sa.Column('numberplate', sa.String(length=32), nullable=False),
    sa.Column('rentable', sa.Boolean(), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('manufacturer', sa.String(length=32), nullable=False),
    sa.Column('model', sa.String(length=32), nullable=False),
    sa.Column('color', sa.String(length=32), nullable=False),
    sa.Column('seats', sa.Integer(), nullable=False),
    sa.Column('pictures', sa.String(length=100), nullable=False),
    sa.Column('interior', sa.String(length=32), nullable=False),
    sa.Column('bodytype', sa.String(length=32), nullable=False),
    sa.Column('gearbox', sa.String(length=32), nullable=False),
    sa.Column('doors', sa.Integer(), nullable=False),
    sa.Column('fueltype', sa.String(length=32), nullable=False),
    sa.Column('topspeed', sa.Integer(), nullable=False),
    sa.Column('power', sa.Integer(), nullable=False),
    sa.Column('torque', sa.Integer(), nullable=False),
    sa.Column('enginetype', sa.String(length=32), nullable=False),
    sa.Column('extras', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('carid')
    )
    op.create_table('Rentals',
    sa.Column('carid', sa.Integer(), nullable=False),
    sa.Column('renterid', sa.Integer(), nullable=False),
    sa.Column('rentstatus', sa.String(length=20), nullable=False),
    sa.Column('rentduration', sa.Integer(), nullable=False),
    sa.Column('rentprice', sa.Integer(), nullable=False),
    sa.Column('renteraddress', sa.String(length=100), nullable=False),
    sa.Column('renterphonenum', sa.String(length=32), nullable=False),
    sa.PrimaryKeyConstraint('carid', 'renterid')
    )
    op.create_table('Roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('role_name', sa.String(length=32), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('Users', schema=None) as batch_op:
        batch_op.alter_column('username',
               existing_type=sa.VARCHAR(length=100),
               type_=sa.String(length=32),
               existing_nullable=False)
        batch_op.alter_column('password',
               existing_type=sa.VARCHAR(length=100),
               type_=sa.String(length=256),
               existing_nullable=False)
        batch_op.alter_column('email',
               existing_type=sa.VARCHAR(length=100),
               type_=sa.String(length=32),
               existing_nullable=False)
        batch_op.alter_column('phone_number',
               existing_type=sa.VARCHAR(length=100),
               type_=sa.String(length=32),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Users', schema=None) as batch_op:
        batch_op.alter_column('phone_number',
               existing_type=sa.String(length=32),
               type_=sa.VARCHAR(length=100),
               existing_nullable=False)
        batch_op.alter_column('email',
               existing_type=sa.String(length=32),
               type_=sa.VARCHAR(length=100),
               existing_nullable=False)
        batch_op.alter_column('password',
               existing_type=sa.String(length=256),
               type_=sa.VARCHAR(length=100),
               existing_nullable=False)
        batch_op.alter_column('username',
               existing_type=sa.String(length=32),
               type_=sa.VARCHAR(length=100),
               existing_nullable=False)

    op.drop_table('Roles')
    op.drop_table('Rentals')
    op.drop_table('Cars')
    # ### end Alembic commands ###
