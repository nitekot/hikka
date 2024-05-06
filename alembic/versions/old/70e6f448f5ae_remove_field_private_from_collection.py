"""Remove field private from collection

Revision ID: 70e6f448f5ae
Revises: 97f5d83e8faf
Create Date: 2024-03-28 18:38:48.915049

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '70e6f448f5ae'
down_revision = '97f5d83e8faf'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('service_collections', 'private')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('service_collections', sa.Column('private', sa.BOOLEAN(), server_default=sa.text('false'), autoincrement=False, nullable=False))
    # ### end Alembic commands ###