"""Đạo Thụ: một buổi luyện / Thiên kiếp nhỏ thuộc về một nút của cây giáo trình (node_id)

Revision ID: 0016_math_tree
Revises: 0015_math_ladder
Create Date: 2026-11-19 18:00:00
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = '0016_math_tree'
down_revision: Union[str, None] = '0015_math_ladder'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table('math_runs', schema=None) as batch_op:
        batch_op.add_column(sa.Column('node_id', sa.String(length=40), nullable=True))
        batch_op.create_index('ix_math_runs_node', ['user_id', 'node_id'], unique=False)


def downgrade() -> None:
    with op.batch_alter_table('math_runs', schema=None) as batch_op:
        batch_op.drop_index('ix_math_runs_node')
        batch_op.drop_column('node_id')
