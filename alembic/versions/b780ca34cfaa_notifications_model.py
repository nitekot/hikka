"""Notifications model

Revision ID: b780ca34cfaa
Revises: 32046c7c41ff
Create Date: 2024-02-10 18:38:32.631913

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b780ca34cfaa'
down_revision = '32046c7c41ff'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('service_notifications',
    sa.Column('notification_type', sa.String(length=64), nullable=False),
    sa.Column('target_id', sa.Uuid(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=False),
    sa.Column('seen', sa.Boolean(), nullable=False),
    sa.Column('log_id', sa.Uuid(), nullable=True),
    sa.Column('user_id', sa.Uuid(), nullable=True),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(['log_id'], ['service_logs.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['service_users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_service_notifications_created'), 'service_notifications', ['created'], unique=False)
    op.create_index(op.f('ix_service_notifications_notification_type'), 'service_notifications', ['notification_type'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_service_notifications_notification_type'), table_name='service_notifications')
    op.drop_index(op.f('ix_service_notifications_created'), table_name='service_notifications')
    op.drop_table('service_notifications')
    # ### end Alembic commands ###
