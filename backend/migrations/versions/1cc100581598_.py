"""empty message

Revision ID: 1cc100581598
Revises: 36b28a3fe64d
Create Date: 2025-04-03 20:39:53.935900

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1cc100581598'
down_revision: Union[str, None] = '36b28a3fe64d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('students',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('student_id', sa.String(length=50), nullable=True),
    sa.Column('major', sa.String(length=50), nullable=True),
    sa.Column('year', sa.String(length=50), nullable=True),
    sa.Column('grade', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_students_grade'), 'students', ['grade'], unique=False)
    op.create_index(op.f('ix_students_id'), 'students', ['id'], unique=False)
    op.create_index(op.f('ix_students_major'), 'students', ['major'], unique=False)
    op.create_index(op.f('ix_students_name'), 'students', ['name'], unique=False)
    op.create_index(op.f('ix_students_student_id'), 'students', ['student_id'], unique=False)
    op.create_index(op.f('ix_students_year'), 'students', ['year'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_students_year'), table_name='students')
    op.drop_index(op.f('ix_students_student_id'), table_name='students')
    op.drop_index(op.f('ix_students_name'), table_name='students')
    op.drop_index(op.f('ix_students_major'), table_name='students')
    op.drop_index(op.f('ix_students_id'), table_name='students')
    op.drop_index(op.f('ix_students_grade'), table_name='students')
    op.drop_table('students')
    # ### end Alembic commands ###
