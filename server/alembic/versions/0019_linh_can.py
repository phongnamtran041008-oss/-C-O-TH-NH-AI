"""Linh căn: mỗi người chơi một dòng - linh căn đang mang, linh căn chờ chọn, bảo hiểm theo đan, đồ giám (linh_can)

Revision ID: 0019_linh_can
Revises: 0018_weapon_claims
Create Date: 2026-11-20 23:00:00
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = '0019_linh_can'
down_revision: Union[str, None] = '0018_weapon_claims'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('linh_can',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('root_id', sa.String(length=40), nullable=True),
    sa.Column('pending_id', sa.String(length=40), nullable=True),
    sa.Column('pending_pill', sa.String(length=40), nullable=True),
    sa.Column('pity', sa.JSON(), nullable=False),
    sa.Column('rolls', sa.Integer(), nullable=False),
    sa.Column('discovered', sa.JSON(), nullable=False),
    sa.Column('awakened_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id')
    )


def downgrade() -> None:
    op.drop_table('linh_can')
