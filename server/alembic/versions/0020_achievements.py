"""Thành Tựu: bộ đếm của mỗi người chơi (achievement_counters) và các thành tựu đã đạt (achievements)

Revision ID: 0020_achievements
Revises: 0019_linh_can
Create Date: 2026-11-21 10:00:00
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = '0020_achievements'
down_revision: Union[str, None] = '0019_linh_can'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('achievement_counters',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('key', sa.String(length=80), nullable=False),
    sa.Column('value', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'key')
    )
    op.create_table('achievements',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('ach_id', sa.String(length=40), nullable=False),
    sa.Column('tier', sa.Integer(), nullable=False),
    sa.Column('claimed', sa.Integer(), nullable=False),
    sa.Column('seen', sa.Integer(), nullable=False),
    sa.Column('unlocked_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'ach_id')
    )


def downgrade() -> None:
    op.drop_table('achievements')
    op.drop_table('achievement_counters')
