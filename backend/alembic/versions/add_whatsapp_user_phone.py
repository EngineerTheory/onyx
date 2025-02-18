"""Add WhatsApp phone number to User

Revision ID: add_whatsapp_user_phone
Revises: add_whatsapp_tables
Create Date: ${current_date}

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_whatsapp_user_phone'
down_revision = 'add_whatsapp_tables'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add WhatsApp phone number column to user table
    op.add_column(
        'user',
        sa.Column('whatsapp_phone_number', sa.String(), nullable=True)
    )
    op.create_unique_constraint(
        'uq_user_whatsapp_phone_number',
        'user',
        ['whatsapp_phone_number']
    )


def downgrade() -> None:
    op.drop_constraint('uq_user_whatsapp_phone_number', 'user', type_='unique')
    op.drop_column('user', 'whatsapp_phone_number')
