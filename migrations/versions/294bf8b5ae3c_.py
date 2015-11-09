"""empty message

Revision ID: 294bf8b5ae3c
Revises: 782db78f6e3
Create Date: 2015-11-08 21:09:43.562690

"""

# revision identifiers, used by Alembic.
revision = '294bf8b5ae3c'
down_revision = '782db78f6e3'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('contacts', sa.Column('comment', sa.Text(), nullable=True))
    op.alter_column('contacts', 'email',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('contacts', 'phone',
               existing_type=sa.VARCHAR(),
               nullable=True)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('contacts', 'phone',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('contacts', 'email',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.drop_column('contacts', 'comment')
    ### end Alembic commands ###
