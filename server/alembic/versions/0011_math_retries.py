"""Math mistakes that come back as parallel questions (M3, learning-path rule 6)

Revision ID: 0011
Revises: 0010
Create Date: 2026-11-14 10:00:00
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = '0011'
down_revision: Union[str, None] = '0010'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('math_retries',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('subject_id', sa.String(length=40), nullable=False),
    sa.Column('floor', sa.Integer(), nullable=False),
    sa.Column('skill_id', sa.String(length=40), nullable=False),
    sa.Column('tier', sa.Integer(), nullable=False),
    sa.Column('item_id', sa.String(length=40), nullable=False),
    sa.Column('fingerprint', sa.String(length=64), nullable=False),
    sa.Column('after_answer_id', sa.Integer(), nullable=False),
    sa.Column('misses', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('cleared_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('math_retries', schema=None) as batch_op:
        batch_op.create_index('ix_math_retries_open', ['user_id', 'subject_id', 'floor', 'cleared_at'], unique=False)


def downgrade() -> None:
    with op.batch_alter_table('math_retries', schema=None) as batch_op:
        batch_op.drop_index('ix_math_retries_open')
    op.drop_table('math_retries')
