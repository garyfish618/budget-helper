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
    op.add_column('budget_month', sa.Column('extra_income', sa.String, server_default="0", nullable=False))



def downgrade():
    op.drop_column('budget_month', 'extra_income')
    op.add_column('budget_month', sa.Column('extra_income', sa.String))