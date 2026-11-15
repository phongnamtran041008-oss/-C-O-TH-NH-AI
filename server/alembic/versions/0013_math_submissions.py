"""Bài tập lập trình: the go at an exercise and its verdict (M6)

Revision ID: 0013
Revises: 0012
Create Date: 2026-11-14 13:00:00
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = '0013'
down_revision: Union[str, None] = '0012'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('math_submissions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('problem_id', sa.String(length=40), nullable=False),
    sa.Column('subject_id', sa.String(length=40), nullable=False),
    sa.Column('floor', sa.Integer(), nullable=False),
    sa.Column('tier', sa.Integer(), nullable=False),
    sa.Column('verdict', sa.String(length=4), nullable=True),
    sa.Column('passed', sa.Integer(), nullable=False),
    sa.Column('total', sa.Integer(), nullable=False),
    sa.Column('ms', sa.Integer(), nullable=False),
    sa.Column('xp_gained', sa.Integer(), nullable=False),
    sa.Column('code', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('judged_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('math_submissions', schema=None) as batch_op:
        batch_op.create_index('ix_math_submissions_user', ['user_id', 'problem_id', 'id'], unique=False)


def downgrade() -> None:
    with op.batch_alter_table('math_submissions', schema=None) as batch_op:
        batch_op.drop_index('ix_math_submissions_user')
    op.drop_table('math_submissions')
