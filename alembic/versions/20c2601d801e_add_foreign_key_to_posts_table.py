"""add foreign-key to posts table

Revision ID: 20c2601d801e
Revises: fa29aa89be61
Create Date: 2022-11-21 12:48:02.426764

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20c2601d801e'
down_revision = 'fa29aa89be61'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('created_by', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table='posts', referent_table='users',
    local_cols=['created_by'], remote_cols=['id'], ondelete="CASCADE")
    pass

def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name='posts')
    op.drop_column('posts', 'created_by')
    pass
