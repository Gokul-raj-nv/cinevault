"""add vectors and delete rules

Revision ID: 41d8c6f0b2aa
Revises: 26eff4a8c8cd
Create Date: 2026-08-29
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector


revision: str = "41d8c6f0b2aa"
down_revision: Union[str, Sequence[str], None] = "26eff4a8c8cd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")
    op.add_column("movies", sa.Column("embedding", Vector(384), nullable=True))

    op.drop_constraint("movies_genre_id_fkey", "movies", type_="foreignkey")
    op.create_foreign_key("movies_genre_id_fkey", "movies", "genres", ["genre_id"], ["id"], ondelete="SET NULL")

    for table, column, target in (
        ("movie_actors", "movie_id", "movies"),
        ("movie_actors", "actor_id", "actors"),
        ("ratings", "user_id", "users"),
        ("ratings", "movie_id", "movies"),
        ("watchlist", "user_id", "users"),
        ("watchlist", "movie_id", "movies"),
        ("watch_history", "user_id", "users"),
        ("watch_history", "movie_id", "movies"),
    ):
        constraint_name = f"{table}_{column}_fkey"
        op.drop_constraint(constraint_name, table, type_="foreignkey")
        op.create_foreign_key(constraint_name, table, target, [column], ["id"], ondelete="CASCADE")

    op.create_unique_constraint("uq_user_movie_history", "watch_history", ["user_id", "movie_id"])


def downgrade() -> None:
    op.drop_constraint("uq_user_movie_history", "watch_history", type_="unique")

    for table, column, target in (
        ("watch_history", "movie_id", "movies"),
        ("watch_history", "user_id", "users"),
        ("watchlist", "movie_id", "movies"),
        ("watchlist", "user_id", "users"),
        ("ratings", "movie_id", "movies"),
        ("ratings", "user_id", "users"),
        ("movie_actors", "actor_id", "actors"),
        ("movie_actors", "movie_id", "movies"),
    ):
        constraint_name = f"{table}_{column}_fkey"
        op.drop_constraint(constraint_name, table, type_="foreignkey")
        op.create_foreign_key(constraint_name, table, target, [column], ["id"])

    op.drop_constraint("movies_genre_id_fkey", "movies", type_="foreignkey")
    op.create_foreign_key("movies_genre_id_fkey", "movies", "genres", ["genre_id"], ["id"])
    op.drop_column("movies", "embedding")
