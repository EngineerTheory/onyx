"""Add WhatsApp bot tables

Revision ID: add_whatsapp_tables
Revises: ${previous_revision}
Create Date: ${current_date}

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'add_whatsapp_tables'
down_revision = '${previous_revision}'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create whatsapp_bot table
    op.create_table(
        'whatsapp_bot',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('enabled', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('phone_number_id', sa.LargeBinary(), nullable=False),
        sa.Column('access_token', sa.LargeBinary(), nullable=False),
        sa.Column('webhook_token', sa.LargeBinary(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('phone_number_id'),
        sa.UniqueConstraint('access_token'),
        sa.UniqueConstraint('webhook_token')
    )

    # Create whatsapp_chat_config table
    op.create_table(
        'whatsapp_chat_config',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('whatsapp_bot_id', sa.Integer(), nullable=False),
        sa.Column('persona_id', sa.Integer(), nullable=True),
        sa.Column('chat_id', sa.String(), nullable=False),
        sa.Column('chat_name', sa.String(), nullable=True),
        sa.Column('chat_type', sa.String(), nullable=False),
        sa.Column('enable_auto_filters', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('is_default', sa.Boolean(), server_default='false', nullable=False),
        sa.ForeignKeyConstraint(['whatsapp_bot_id'], ['whatsapp_bot.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['persona_id'], ['persona.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('whatsapp_bot_id', 'is_default', name='uq_whatsapp_chat_config_whatsapp_bot_id_default')
    )

    # Create index for default config lookup
    op.create_index(
        'ix_whatsapp_chat_config_whatsapp_bot_id_default',
        'whatsapp_chat_config',
        ['whatsapp_bot_id', 'is_default'],
        unique=True,
        postgresql_where=sa.text('is_default IS TRUE')
    )


def downgrade() -> None:
    op.drop_index('ix_whatsapp_chat_config_whatsapp_bot_id_default')
    op.drop_table('whatsapp_chat_config')
    op.drop_table('whatsapp_bot')
