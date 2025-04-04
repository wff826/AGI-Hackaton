"""empty message

Revision ID: 8017278a7926
Revises: 7d2352dfad5d
Create Date: 2025-04-03 21:58:54.974483

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8017278a7926'
down_revision: Union[str, None] = '7d2352dfad5d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('scholarships',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('raw_text', sa.JSON(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_scholarships_id'), 'scholarships', ['id'], unique=False)
    op.create_index(op.f('ix_scholarships_name'), 'scholarships', ['name'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_scholarships_name'), table_name='scholarships')
    op.drop_index(op.f('ix_scholarships_id'), table_name='scholarships')
    op.drop_table('scholarships')
    # ### end Alembic commands ###
