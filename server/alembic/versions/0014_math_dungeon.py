"""Hầm ngục: one trip into a seeded dungeon (M10)

Revision ID: 0014_math_dungeon
Revises: 0013
Create Date: 2026-11-18 10:00:00
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = '0014_math_dungeon'
down_revision: Union[str, None] = '0013'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('math_dungeon_runs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('seed', sa.Integer(), nullable=False),
    sa.Column('subject_id', sa.String(length=40), nullable=False),
    sa.Column('floor', sa.Integer(), nullable=False),
    sa.Column('layout', sa.JSON(), nullable=False),
    sa.Column('room', sa.Integer(), nullable=False),
    sa.Column('progress', sa.Integer(), nullable=False),
    sa.Column('hearts', sa.Integer(), nullable=False),
    sa.Column('max_hearts', sa.Integer(), nullable=False),
    sa.Column('state', sa.String(length=10), nullable=False),
    sa.Column('asked', sa.Integer(), nullable=False),
    sa.Column('correct', sa.Integer(), nullable=False),
    sa.Column('xp_gained', sa.Integer(), nullable=False),
    sa.Column('stones_gained', sa.Integer(), nullable=False),
    sa.Column('items_gained', sa.JSON(), nullable=False),
    sa.Column('rewarded', sa.Boolean(), nullable=False),
    sa.Column('started_at', sa.DateTime(), nullable=False),
    sa.Column('ended_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('math_dungeon_runs', schema=None) as batch_op:
        batch_op.create_index('ix_math_dungeon_runs_user', ['user_id', 'ended_at'], unique=False)
        batch_op.create_index('ix_math_dungeon_runs_day', ['user_id', 'started_at'], unique=False)


def downgrade() -> None:
    with op.batch_alter_table('math_dungeon_runs', schema=None) as batch_op:
        batch_op.drop_index('ix_math_dungeon_runs_day')
        batch_op.drop_index('ix_math_dungeon_runs_user')
    op.drop_table('math_dungeon_runs')
