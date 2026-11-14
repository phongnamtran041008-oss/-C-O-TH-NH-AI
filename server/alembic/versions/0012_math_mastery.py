"""Mastery gates, the Thiên kiếp nhỏ and spiral review (M5, learning-path rules 3 and 6)

Adds to math_runs: mode (practice|trial), passed (a trial's verdict) and review_asked
(how many questions of the sitting were spiral review), and to math_answers: review.
The sittings and answers already in the table are ordinary practice, which is what the
defaults say, so nothing is rewritten.

Revision ID: 0012
Revises: 0011
Create Date: 2026-11-14 11:00:00
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = '0012'
down_revision: Union[str, None] = '0011'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table('math_runs', schema=None) as batch_op:
        batch_op.add_column(sa.Column('mode', sa.String(length=10), nullable=False,
                                      server_default='practice'))
        batch_op.add_column(sa.Column('review_asked', sa.Integer(), nullable=False, server_default='0'))
        batch_op.add_column(sa.Column('passed', sa.Boolean(), nullable=True))
        batch_op.create_index('ix_math_runs_cleared', ['user_id', 'subject_id', 'mode', 'passed'],
                              unique=False)
    with op.batch_alter_table('math_answers', schema=None) as batch_op:
        batch_op.add_column(sa.Column('review', sa.Boolean(), nullable=False, server_default=sa.false()))


def downgrade() -> None:
    with op.batch_alter_table('math_answers', schema=None) as batch_op:
        batch_op.drop_column('review')
    with op.batch_alter_table('math_runs', schema=None) as batch_op:
        batch_op.drop_index('ix_math_runs_cleared')
        batch_op.drop_column('passed')
        batch_op.drop_column('review_asked')
        batch_op.drop_column('mode')
