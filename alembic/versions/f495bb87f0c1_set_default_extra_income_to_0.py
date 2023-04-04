"""Set default extra income to 0

Revision ID: f495bb87f0c1
Revises: 7bbd5c3df2a3
Create Date: 2023-04-03 16:47:55.837574

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f495bb87f0c1'
down_revision = '7bbd5c3df2a3'
branch_labels = None
depends_on = None

default_value = "0"

def upgrade():
    op.execute("ALTER TABLE budget_month ALTER COLUMN extra_income SET DEFAULT '0';")
    op.execute("UPDATE budget_month SET extra_income = '0' WHERE extra_income IS NULL;")
    op.execute("ALTER TABLE budget_month ALTER COLUMN extra_income SET NOT NULL;")


def downgrade():
    # Set the extra_income column back to its original state
    op.execute("ALTER TABLE budget_month ALTER COLUMN extra_income DROP NOT NULL;")
    op.execute("ALTER TABLE budget_month ALTER COLUMN extra_income DROP DEFAULT;")
