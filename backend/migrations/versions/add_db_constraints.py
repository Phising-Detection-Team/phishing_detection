"""Add DB-level CHECK and UNIQUE constraints to models.

Revision ID: add_db_constraints
Revises: f68964d2d980
Create Date: 2026-02-12 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_db_constraints'
down_revision = 'da9729d5d670'
branch_labels = None
depends_on = None

# upgrade will add CHECK constraints to enforce data integrity at the database level, and a UNIQUE constraint for Manual_Overrides.email_test_id
def upgrade():
    bind = op.get_bind()     # Get current DB connection to check dialect
    is_sqlite = bind.dialect.name == 'sqlite'

    # helper to apply create constraint either directly or with batch for sqlite
    def create_check(name, table, sql):
        if is_sqlite:
            # SQLite doesn't support ALTER TABLE ADD CONSTRAINT, so we have to use batch mode
            # batch_alter_table will create a new table with the constraint, copy data, drop old table, and rename new table
            with op.batch_alter_table(table) as batch_op:
                batch_op.create_check_constraint(name, sql)
        else:
            op.create_check_constraint(name, table, sql)

    # SQLite doesn't support ALTER TABLE ADD CONSTRAINT for UNIQUE constraints either, so we need a helper for that as well
    def create_unique(name, table, cols):
        if is_sqlite:
            with op.batch_alter_table(table) as batch_op:
                batch_op.create_unique_constraint(name, cols)
        else:
            op.create_unique_constraint(name, table, cols)

    # Create constraints for all models
    # Emails
    create_check('ck_email_detector_confidence_range', 'Emails', 'detector_confidence >= 0 AND detector_confidence <= 1')
    create_check('ck_email_generator_latency_nonneg', 'Emails', 'generator_latency_ms IS NULL OR generator_latency_ms >= 0')
    create_check('ck_email_detector_latency_nonneg', 'Emails', 'detector_latency_ms IS NULL OR detector_latency_ms >= 0')
    create_check('ck_email_cost_nonneg', 'Emails', 'cost IS NULL OR cost >= 0')
    create_check('ck_email_detector_verdict_enum', 'Emails', "detector_verdict IN ('phishing','legitimate')")
    create_check('ck_email_processing_time_nonneg', 'Emails', 'processing_time IS NULL OR processing_time >= 0')

    # Rounds
    create_check('ck_round_total_emails_positive', 'Rounds', 'total_emails > 0')
    create_check('ck_round_processed_emails_nonneg', 'Rounds', 'processed_emails >= 0')
    create_check('ck_round_processed_le_total', 'Rounds', 'processed_emails <= total_emails')
    create_check('ck_round_status_enum', 'Rounds', "status IN ('pending','running','completed','failed')")
    create_check('ck_round_detector_accuracy_range', 'Rounds', 'detector_accuracy IS NULL OR (detector_accuracy >= 0 AND detector_accuracy <= 100)')
    create_check('ck_round_generator_success_range', 'Rounds', 'generator_success_rate IS NULL OR (generator_success_rate >= 0 AND generator_success_rate <= 100)')
    create_check('ck_round_avg_confidence_range', 'Rounds', 'avg_confidence_score IS NULL OR (avg_confidence_score >= 0 AND avg_confidence_score <= 100)')
    create_check('ck_round_total_cost_nonneg', 'Rounds', 'total_cost >= 0')

    # Logs
    create_check('ck_log_level_enum', 'Logs', "level IN ('info','warning','error','critical')")

    # API_calls
    create_check('ck_api_agent_type_enum', 'API_calls', "agent_type IN ('generator','detector','judge')")
    create_check('ck_api_token_used_nonneg', 'API_calls', 'token_used IS NULL OR token_used >= 0')
    create_check('ck_api_cost_nonneg', 'API_calls', 'cost IS NULL OR cost >= 0')
    create_check('ck_api_latency_nonneg', 'API_calls', 'latency_ms IS NULL OR latency_ms >= 0')

    # Manual_Overrides
    create_check('ck_override_verdict_enum', 'Manual_Overrides', "verdict IN ('correct','incorrect','phishing','legitimate')")
    create_unique('uq_override_email_test_id', 'Manual_Overrides', ['email_test_id'])

# Note: Downgrade will drop these constraints but keep the columns intact, so we won't lose any data if we need to revert
def downgrade():
    # Drop all constraints (order matters for dependencies)
    op.drop_constraint('uq_override_email_test_id', 'Manual_Overrides', type_='unique')
    op.drop_constraint('ck_override_verdict_enum', 'Manual_Overrides', type_='check')

    op.drop_constraint('ck_api_latency_nonneg', 'API_calls', type_='check')
    op.drop_constraint('ck_api_cost_nonneg', 'API_calls', type_='check')
    op.drop_constraint('ck_api_token_used_nonneg', 'API_calls', type_='check')
    op.drop_constraint('ck_api_agent_type_enum', 'API_calls', type_='check')

    op.drop_constraint('ck_log_level_enum', 'Logs', type_='check')

    op.drop_constraint('ck_round_total_cost_nonneg', 'Rounds', type_='check')
    op.drop_constraint('ck_round_avg_confidence_range', 'Rounds', type_='check')
    op.drop_constraint('ck_round_generator_success_range', 'Rounds', type_='check')
    op.drop_constraint('ck_round_detector_accuracy_range', 'Rounds', type_='check')
    op.drop_constraint('ck_round_status_enum', 'Rounds', type_='check')
    op.drop_constraint('ck_round_processed_le_total', 'Rounds', type_='check')
    op.drop_constraint('ck_round_processed_emails_nonneg', 'Rounds', type_='check')
    op.drop_constraint('ck_round_total_emails_positive', 'Rounds', type_='check')

    op.drop_constraint('ck_email_processing_time_nonneg', 'Emails', type_='check')
    op.drop_constraint('ck_email_detector_verdict_enum', 'Emails', type_='check')
    op.drop_constraint('ck_email_cost_nonneg', 'Emails', type_='check')
    op.drop_constraint('ck_email_detector_latency_nonneg', 'Emails', type_='check')
    op.drop_constraint('ck_email_generator_latency_nonneg', 'Emails', type_='check')
    op.drop_constraint('ck_email_detector_confidence_range', 'Emails', type_='check')