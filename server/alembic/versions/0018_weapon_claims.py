"""Binh khí của Thiên Địa Đồ: mỗi chỗ đặt vũ khí chỉ cho mỗi người chơi một lần (weapon_claims)

Revision ID: 0018_weapon_claims
Revises: 0017_drop_word_game
Create Date: 2026-11-20 20:00:00
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = '0018_weapon_claims'
down_revision: Union[str, None] = '0017_drop_word_game'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('weapon_claims',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('placed_id', sa.String(length=48), nullable=False),
    sa.Column('instance_id', sa.Integer(), nullable=True),
    sa.Column('claimed_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id', 'placed_id')
    )
    with op.batch_alter_table('weapon_claims', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_weapon_claims_user_id'), ['user_id'], unique=False)


def downgrade() -> None:
    with op.batch_alter_table('weapon_claims', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_weapon_claims_user_id'))
    op.drop_table('weapon_claims')
