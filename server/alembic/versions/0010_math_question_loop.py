"""Math question loop (M2): quiz_sessions.word_id becomes item_id, math runs and answers

quiz_sessions.word_id was a foreign key to words, so only vocabulary questions fitted in
the question log. It is renamed to item_id and the foreign key is dropped: a vocabulary
question still stores its word id there, a math question stores its math item id. qtype
grows from 4 to 20 characters for the math question types ("multiple_choice", ...).

Revision ID: 0010
Revises: 0009
Create Date: 2026-11-13 22:00:00
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = '0010'
down_revision: Union[str, None] = '0009'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

_FK = "fk_quiz_sessions_word_id_words"      # the name the key gets when a downgrade puts it back


def _quiz_sessions(id_column: str, qtype_length: int) -> sa.Table:
    """quiz_sessions without the foreign key to words. SQLite cannot drop a column's
    foreign key in place, and the key 0001 created there has no name to drop it by, so the
    table is rebuilt from this description instead of from what the database reports."""
    return sa.Table(
        'quiz_sessions', sa.MetaData(),
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('context', sa.String(length=16), nullable=False),
        sa.Column('ref', sa.String(length=64), nullable=True),
        sa.Column('qtype', sa.String(length=qtype_length), nullable=False),
        sa.Column(id_column, sa.String(length=40), nullable=False),
        sa.Column('payload', sa.JSON(), nullable=False),
        sa.Column('answer_key', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('expires_at', sa.DateTime(), nullable=False),
        sa.Column('answered_at', sa.DateTime(), nullable=True),
        sa.Column('correct', sa.Boolean(), nullable=True),
        sa.Column('answer', sa.JSON(), nullable=True),
        sa.Column('answer_ms', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.Index('ix_quiz_user_created', 'user_id', 'created_at'),
    )


def _is_sqlite() -> bool:
    return op.get_bind().dialect.name == "sqlite"


def _word_fk_name() -> str | None:
    """The name of the quiz_sessions.word_id -> words.id key (PostgreSQL names it
    quiz_sessions_word_id_fkey by itself)."""
    for fk in sa.inspect(op.get_bind()).get_foreign_keys("quiz_sessions"):
        if fk.get("constrained_columns") == ["word_id"] and fk.get("name"):
            return fk["name"]
    return None


def upgrade() -> None:
    if _is_sqlite():
        with op.batch_alter_table('quiz_sessions', copy_from=_quiz_sessions('word_id', 4),
                                  recreate='always') as batch:
            batch.alter_column('word_id', new_column_name='item_id')
            batch.alter_column('qtype', type_=sa.String(length=20))
    else:
        fk = _word_fk_name()
        if fk:
            op.drop_constraint(fk, 'quiz_sessions', type_='foreignkey')
        op.alter_column('quiz_sessions', 'word_id', new_column_name='item_id')
        op.alter_column('quiz_sessions', 'qtype', type_=sa.String(length=20),
                        existing_type=sa.String(length=4), existing_nullable=False)

    op.create_table('math_runs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('subject_id', sa.String(length=40), nullable=False),
    sa.Column('floor', sa.Integer(), nullable=False),
    sa.Column('tier', sa.Integer(), nullable=False),
    sa.Column('correct_streak', sa.Integer(), nullable=False),
    sa.Column('wrong_streak', sa.Integer(), nullable=False),
    sa.Column('combo', sa.Integer(), nullable=False),
    sa.Column('best_combo', sa.Integer(), nullable=False),
    sa.Column('asked', sa.Integer(), nullable=False),
    sa.Column('correct', sa.Integer(), nullable=False),
    sa.Column('xp_gained', sa.Integer(), nullable=False),
    sa.Column('started_at', sa.DateTime(), nullable=False),
    sa.Column('ended_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('math_runs', schema=None) as batch_op:
        batch_op.create_index('ix_math_runs_user_open', ['user_id', 'ended_at'], unique=False)

    op.create_table('math_answers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('run_id', sa.Integer(), nullable=True),
    sa.Column('subject_id', sa.String(length=40), nullable=False),
    sa.Column('skill_id', sa.String(length=40), nullable=False),
    sa.Column('floor', sa.Integer(), nullable=False),
    sa.Column('tier', sa.Integer(), nullable=False),
    sa.Column('item_id', sa.String(length=40), nullable=False),
    sa.Column('qtype', sa.String(length=20), nullable=False),
    sa.Column('fingerprint', sa.String(length=64), nullable=False),
    sa.Column('correct', sa.Boolean(), nullable=False),
    sa.Column('timed_out', sa.Boolean(), nullable=False),
    sa.Column('answer_ms', sa.Integer(), nullable=False),
    sa.Column('answered_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['run_id'], ['math_runs.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('math_answers', schema=None) as batch_op:
        batch_op.create_index('ix_math_answers_skill', ['user_id', 'skill_id', 'tier', 'id'], unique=False)


def downgrade() -> None:
    with op.batch_alter_table('math_answers', schema=None) as batch_op:
        batch_op.drop_index('ix_math_answers_skill')
    op.drop_table('math_answers')
    with op.batch_alter_table('math_runs', schema=None) as batch_op:
        batch_op.drop_index('ix_math_runs_user_open')
    op.drop_table('math_runs')

    # math questions cannot go back: their item ids are not words and their type names
    # do not fit in 4 characters
    op.execute("DELETE FROM quiz_sessions WHERE context = 'math'")
    if _is_sqlite():
        with op.batch_alter_table('quiz_sessions', copy_from=_quiz_sessions('item_id', 20),
                                  recreate='always') as batch:
            batch.alter_column('qtype', type_=sa.String(length=4))
            batch.alter_column('item_id', new_column_name='word_id')
        # a second rebuild: a key added in the same batch as the rename is silently lost
        with op.batch_alter_table('quiz_sessions', copy_from=_quiz_sessions('word_id', 4),
                                  recreate='always') as batch:
            batch.create_foreign_key(_FK, 'words', ['word_id'], ['id'])
    else:
        op.alter_column('quiz_sessions', 'qtype', type_=sa.String(length=4),
                        existing_type=sa.String(length=20), existing_nullable=False)
        op.alter_column('quiz_sessions', 'item_id', new_column_name='word_id')
        op.create_foreign_key(_FK, 'quiz_sessions', 'words', ['word_id'], ['id'])
