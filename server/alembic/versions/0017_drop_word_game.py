"""Drop what is left of the old word game: its tables, dead columns, two honest names

The garden, the word collection, word skills, crafted sentences and the word tower defence
loadout are gone from the game (waves 1-3 of the purge, docs/DECISIONS.md 2026-11-20), so
their tables go: words, plots, seeds, collection, fruits, crafted_sentences, skills,
td_loadout. Columns nothing reads any more go too: equipment_instances.inscriptions
(engraving), hive.pollen_checked_at (pollination), friendships.help_count_date/help_count
(watering a friend's garden), users.current_letter_id (the garden letters).

Two columns kept their old-game names although they hold something else now:
users.daily_new_seeds_count is the gacha's daily roll counter -> daily_rolls_count;
tribulation_runs.words held one placeholder per question -> an integer `total`.

The downgrade puts every table back empty with its old schema (the word rows cannot come
back) and every column back with its old default.

Revision ID: 0017_drop_word_game
Revises: 0016_math_tree
Create Date: 2026-11-20 12:00:00
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = '0017_drop_word_game'
down_revision: Union[str, None] = '0016_math_tree'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# children first: plots, seeds, collection and fruits have a foreign key to words
_TABLES = ('plots', 'seeds', 'collection', 'fruits', 'crafted_sentences', 'skills', 'td_loadout', 'words')
_INDEXED = {'plots': 'ix_plots_user_id', 'seeds': 'ix_seeds_user_id',
            'crafted_sentences': 'ix_crafted_sentences_user_id'}


def _user_fk() -> sa.ForeignKeyConstraint:
    return sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE')


def upgrade() -> None:
    bind = op.get_bind()
    for table in _TABLES:
        if table in _INDEXED:
            with op.batch_alter_table(table, schema=None) as batch_op:
                batch_op.drop_index(_INDEXED[table])
        op.drop_table(table)

    with op.batch_alter_table('equipment_instances', schema=None) as batch_op:
        batch_op.drop_column('inscriptions')
    with op.batch_alter_table('hive', schema=None) as batch_op:
        batch_op.drop_column('pollen_checked_at')
    with op.batch_alter_table('friendships', schema=None) as batch_op:
        batch_op.drop_column('help_count_date')
        batch_op.drop_column('help_count')
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('current_letter_id')
        batch_op.alter_column('daily_new_seeds_count', new_column_name='daily_rolls_count',
                              existing_type=sa.Integer(), existing_nullable=False)

    # tribulation_runs.words (a JSON list, one entry per question) -> total (its length)
    with op.batch_alter_table('tribulation_runs', schema=None) as batch_op:
        batch_op.add_column(sa.Column('total', sa.Integer(), nullable=False, server_default='0'))
    runs = sa.table('tribulation_runs', sa.column('id', sa.Integer()), sa.column('words', sa.JSON()),
                    sa.column('total', sa.Integer()))
    for run_id, words in bind.execute(sa.select(runs.c.id, runs.c.words)).all():
        bind.execute(runs.update().where(runs.c.id == run_id).values(total=len(words or [])))
    with op.batch_alter_table('tribulation_runs', schema=None) as batch_op:
        batch_op.drop_column('words')


def downgrade() -> None:
    bind = op.get_bind()
    with op.batch_alter_table('tribulation_runs', schema=None) as batch_op:
        batch_op.add_column(sa.Column('words', sa.JSON(), nullable=False, server_default=sa.text("'[]'")))
    runs = sa.table('tribulation_runs', sa.column('id', sa.Integer()), sa.column('words', sa.JSON()),
                    sa.column('total', sa.Integer()))
    for run_id, total in bind.execute(sa.select(runs.c.id, runs.c.total)).all():
        bind.execute(runs.update().where(runs.c.id == run_id).values(words=["math"] * int(total or 0)))
    with op.batch_alter_table('tribulation_runs', schema=None) as batch_op:
        batch_op.drop_column('total')

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('daily_rolls_count', new_column_name='daily_new_seeds_count',
                              existing_type=sa.Integer(), existing_nullable=False)
        batch_op.add_column(sa.Column('current_letter_id', sa.String(length=20), nullable=True))
    with op.batch_alter_table('friendships', schema=None) as batch_op:
        batch_op.add_column(sa.Column('help_count_date', sa.String(length=10), nullable=True))
        batch_op.add_column(sa.Column('help_count', sa.Integer(), nullable=False, server_default='0'))
    with op.batch_alter_table('hive', schema=None) as batch_op:
        batch_op.add_column(sa.Column('pollen_checked_at', sa.DateTime(), nullable=True))
    with op.batch_alter_table('equipment_instances', schema=None) as batch_op:
        batch_op.add_column(sa.Column('inscriptions', sa.JSON(), nullable=False, server_default=sa.text("'[]'")))

    # the tables of 0001 (+ the plot columns of 0002 and 0004), empty
    op.create_table('words',
    sa.Column('id', sa.String(length=40), nullable=False),
    sa.Column('hanzi', sa.String(length=16), nullable=False),
    sa.Column('tier', sa.Integer(), nullable=False),
    sa.Column('rarity', sa.String(length=12), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('td_loadout',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('slots', sa.JSON(), nullable=False),
    _user_fk(),
    sa.PrimaryKeyConstraint('user_id')
    )
    op.create_table('skills',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('skill_id', sa.String(length=32), nullable=False),
    sa.Column('level', sa.Integer(), nullable=False),
    sa.Column('unlocked_at', sa.DateTime(), nullable=False),
    _user_fk(),
    sa.PrimaryKeyConstraint('user_id', 'skill_id')
    )
    op.create_table('crafted_sentences',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('sentence_id', sa.String(length=20), nullable=False),
    sa.Column('crafted_at', sa.DateTime(), nullable=False),
    _user_fk(),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('fruits',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('word_id', sa.String(length=40), nullable=False),
    sa.Column('count', sa.Integer(), nullable=False),
    _user_fk(),
    sa.ForeignKeyConstraint(['word_id'], ['words.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'word_id')
    )
    op.create_table('collection',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('word_id', sa.String(length=40), nullable=False),
    sa.Column('introduced', sa.Boolean(), nullable=False),
    sa.Column('mastery', sa.Integer(), nullable=False),
    sa.Column('times_correct', sa.Integer(), nullable=False),
    sa.Column('times_wrong', sa.Integer(), nullable=False),
    sa.Column('needs_review', sa.Boolean(), nullable=False),
    sa.Column('first_seen_at', sa.DateTime(), nullable=False),
    sa.Column('last_answered_at', sa.DateTime(), nullable=True),
    _user_fk(),
    sa.ForeignKeyConstraint(['word_id'], ['words.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'word_id')
    )
    op.create_table('seeds',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('word_id', sa.String(length=40), nullable=False),
    sa.Column('duplicate', sa.Boolean(), nullable=False),
    sa.Column('source', sa.String(length=20), nullable=False),
    sa.Column('obtained_at', sa.DateTime(), nullable=False),
    _user_fk(),
    sa.ForeignKeyConstraint(['word_id'], ['words.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('plots',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('x', sa.Integer(), nullable=False),
    sa.Column('y', sa.Integer(), nullable=False),
    sa.Column('unlocked', sa.Boolean(), nullable=False),
    sa.Column('word_id', sa.String(length=40), nullable=True),
    sa.Column('stage', sa.Integer(), nullable=False),
    sa.Column('planted_at', sa.DateTime(), nullable=True),
    sa.Column('next_review_at', sa.DateTime(), nullable=True),
    sa.Column('wither', sa.Float(), nullable=False),
    sa.Column('wither_checked_at', sa.DateTime(), nullable=True),
    sa.Column('pollen', sa.Float(), nullable=False),
    sa.Column('pollinated', sa.Boolean(), nullable=False),
    sa.Column('fire_checked_date', sa.String(length=10), nullable=True),
    sa.Column('pollen_boost', sa.Boolean(), nullable=False, server_default=sa.false()),
    _user_fk(),
    sa.ForeignKeyConstraint(['word_id'], ['words.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id', 'x', 'y')
    )
    for table, index in _INDEXED.items():
        with op.batch_alter_table(table, schema=None) as batch_op:
            batch_op.create_index(index, ['user_id'], unique=False)
