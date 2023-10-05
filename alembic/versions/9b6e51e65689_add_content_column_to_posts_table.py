"""add content column to posts table

Revision ID: 9b6e51e65689
Revises: a0a046ea2666
Create Date: 2023-10-04 18:01:07.613135

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9b6e51e65689'
down_revision: Union[str, None] = 'a0a046ea2666'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String, nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
