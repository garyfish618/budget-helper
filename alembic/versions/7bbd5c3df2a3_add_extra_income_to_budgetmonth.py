"""Add extra_income to BudgetMonth

Revision ID: 7bbd5c3df2a3
Revises: 
Create Date: 2023-04-03 16:39:39.221668

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7bbd5c3df2a3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('budget_month', sa.Column('extra_income', sa.String))


def downgrade():
    op.drop_column('budget_month', 'extra_income')
