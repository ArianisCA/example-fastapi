"""add content column to post table

Revision ID: cebba2e1eb2b
Revises: 1c72ddffcd5f
Create Date: 2022-11-21 12:30:07.018917

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cebba2e1eb2b'
down_revision = '1c72ddffcd5f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass

def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
