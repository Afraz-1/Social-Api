"""create table

Revision ID: 34f71e3c296c
Revises: 
Create Date: 2026-09-14 17:36:26.502342

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '34f71e3c296c'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('posts',sa.column('id',sa.Integer(),nullable = False,primary_key = True),
                    sa.column('title',sa.String(),nullable = False))
   


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('posts')

