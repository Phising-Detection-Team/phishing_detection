"""Rename generator_latenc_ms to generator_latency_ms

Revision ID: da9729d5d670
Revises: add_db_constraints
Create Date: 2026-02-16 13:39:19.204053

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'da9729d5d670'
down_revision: Union[str, Sequence[str], None] = 'f68964d2d980'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Rename generator_latenc_ms to generator_latency_ms."""
    # SQLite doesn't support ALTER COLUMN RENAME directly
    # Need to use batch_alter_table
    with op.batch_alter_table('Emails', schema=None) as batch_op:
        batch_op.alter_column('generator_latenc_ms',
                              new_column_name='generator_latency_ms',
                              existing_type=sa.Integer(),
                              nullable=True)


def downgrade() -> None:
    """Rename generator_latency_ms back to generator_latenc_ms."""
    with op.batch_alter_table('Emails', schema=None) as batch_op:
        batch_op.alter_column('generator_latency_ms',
                              new_column_name='generator_latenc_ms',
                              existing_type=sa.Integer(),
                              nullable=True)
