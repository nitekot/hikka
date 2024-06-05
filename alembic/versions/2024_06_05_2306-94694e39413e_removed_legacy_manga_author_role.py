"""Removed legacy manga author role

Revision ID: 94694e39413e
Revises: 4882ac82d08b
Create Date: 2024-06-05 23:06:55.919701

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "94694e39413e"
down_revision = "4882ac82d08b"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(
        "ix_service_content_manga_author_roles_slug",
        table_name="service_content_manga_author_roles",
    )
    op.drop_table("service_relation_manga_author_roles")
    op.drop_table("service_content_manga_author_roles")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "service_relation_manga_author_roles",
        sa.Column("author_id", sa.UUID(), autoincrement=False, nullable=False),
        sa.Column("role_id", sa.UUID(), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(
            ["author_id"],
            ["service_content_manga_authors.id"],
            name="service_relation_manga_author_roles_author_id_fkey",
        ),
        sa.ForeignKeyConstraint(
            ["role_id"],
            ["service_content_manga_author_roles.id"],
            name="service_relation_manga_author_roles_role_id_fkey",
        ),
        sa.PrimaryKeyConstraint(
            "author_id",
            "role_id",
            name="service_relation_manga_author_roles_pkey",
        ),
    )
    op.create_table(
        "service_content_manga_author_roles",
        sa.Column("name_en", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("name_ua", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("weight", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column("id", sa.UUID(), autoincrement=False, nullable=False),
        sa.Column(
            "slug", sa.VARCHAR(length=255), autoincrement=False, nullable=False
        ),
        sa.PrimaryKeyConstraint(
            "id", name="service_content_manga_author_roles_pkey"
        ),
    )
    op.create_index(
        "ix_service_content_manga_author_roles_slug",
        "service_content_manga_author_roles",
        ["slug"],
        unique=False,
    )
    # ### end Alembic commands ###