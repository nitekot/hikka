"""Added deleted and deletion_request to image

Revision ID: 9243b73ca2d0
Revises: 70f0240158f7
Create Date: 2023-12-24 01:45:07.542462

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "9243b73ca2d0"
down_revision = "70f0240158f7"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "service_images",
        sa.Column(
            "deletion_request",
            sa.Boolean(),
            server_default=sa.schema.DefaultClause("false"),
            nullable=False,
        ),
    )
    op.add_column(
        "service_images", sa.Column("deleted", sa.DateTime(), nullable=True)
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("service_images", "deleted")
    op.drop_column("service_images", "deletion_request")
    # ### end Alembic commands ###
