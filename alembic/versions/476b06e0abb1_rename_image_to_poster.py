"""Rename image to poster

Revision ID: 476b06e0abb1
Revises: 725cd4e97eb9
Create Date: 2023-05-29 14:02:24.284399

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '476b06e0abb1'
down_revision = '725cd4e97eb9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('service_content_anime', sa.Column('poster_id', sa.Uuid(), nullable=True))
    op.drop_constraint('service_content_anime_image_id_fkey', 'service_content_anime', type_='foreignkey')
    op.create_foreign_key(None, 'service_content_anime', 'service_images', ['poster_id'], ['id'], ondelete='SET NULL')
    op.drop_column('service_content_anime', 'image_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('service_content_anime', sa.Column('image_id', sa.UUID(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'service_content_anime', type_='foreignkey')
    op.create_foreign_key('service_content_anime_image_id_fkey', 'service_content_anime', 'service_images', ['image_id'], ['id'], ondelete='SET NULL')
    op.drop_column('service_content_anime', 'poster_id')
    # ### end Alembic commands ###