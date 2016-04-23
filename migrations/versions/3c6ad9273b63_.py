"""empty message

Revision ID: 3c6ad9273b63
Revises: None
Create Date: 2015-10-27 21:29:08.795334

"""

# revision identifiers, used by Alembic.
revision = '3c6ad9273b63'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('contacts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )

    op.add_column('contacts', sa.Column('id', sa.Integer(), nullable=False))
    op.add_column('contacts', sa.Column('date_added', sa.DateTime(), nullable=True))
    op.add_column('contacts', sa.Column('phone', sa.String(), nullable=False))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('contacts', 'phone')
    op.drop_column('contacts', 'date_added')
    ### end Alembic commands ###
