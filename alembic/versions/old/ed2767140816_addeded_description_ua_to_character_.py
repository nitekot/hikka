"""Addeded description_ua to character model

Revision ID: ed2767140816
Revises: 4bc89139bee2
Create Date: 2024-02-02 02:04:26.797436

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ed2767140816'
down_revision = '4bc89139bee2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('service_content_characters', sa.Column('description_ua', sa.String(), nullable=True))
    op.drop_column('service_content_characters', 'description')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('service_content_characters', sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('service_content_characters', 'description_ua')
    # ### end Alembic commands ###