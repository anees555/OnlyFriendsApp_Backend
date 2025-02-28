from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = '8d47d8b7d6a3'
down_revision = 'ef379af1c03f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Convert integer values back to boolean properly
    op.execute("ALTER TABLE similarities ALTER COLUMN is_active TYPE BOOLEAN USING (is_active::BOOLEAN)")

def downgrade() -> None:
    # Convert boolean values to integer properly
    op.execute("ALTER TABLE similarities ALTER COLUMN is_active TYPE INTEGER USING (is_active::INTEGER)")

