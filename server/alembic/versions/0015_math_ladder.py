"""Bậc thang của câu bậc 5 (luật 8) và số bậc thang đã leo của một buổi luyện (M11 đợt 2)

Revision ID: 0015_math_ladder
Revises: 0014_math_dungeon
Create Date: 2026-11-18 16:00:00
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = '0015_math_ladder'
down_revision: Union[str, None] = '0014_math_dungeon'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table('math_runs', schema=None) as batch_op:
        batch_op.add_column(sa.Column('ladders', sa.Integer(), server_default='0', nullable=False))
    op.create_table('math_ladders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('subject_id', sa.String(length=40), nullable=False),
    sa.Column('floor', sa.Integer(), nullable=False),
    sa.Column('item_id', sa.String(length=40), nullable=False),
    sa.Column('skill_id', sa.String(length=40), nullable=False),
    sa.Column('steps', sa.JSON(), nullable=False),
    sa.Column('step', sa.Integer(), nullable=False),
    sa.Column('missed', sa.Integer(), nullable=False),
    sa.Column('retry_id', sa.Integer(), nullable=True),
    sa.Column('started_run_id', sa.Integer(), nullable=True),
    sa.Column('run_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('finished_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('math_ladders', schema=None) as batch_op:
        batch_op.create_index('ix_math_ladders_open', ['user_id', 'subject_id', 'floor', 'finished_at'],
                              unique=False)


def downgrade() -> None:
    with op.batch_alter_table('math_ladders', schema=None) as batch_op:
        batch_op.drop_index('ix_math_ladders_open')
    op.drop_table('math_ladders')
    with op.batch_alter_table('math_runs', schema=None) as batch_op:
        batch_op.drop_column('ladders')
