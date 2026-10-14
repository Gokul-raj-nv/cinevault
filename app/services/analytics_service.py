from datetime import datetime, timedelta

from sqlalchemy import func, select, union_all
from sqlalchemy.orm import Session

from app.models.genre import Genre
from app.models.movie import Movie
from app.models.rating import Rating
from app.models.user import User
from app.models.watch_history import WatchHistory
from app.models.watchlist import Watchlist


class AnalyticsService:
    def __init__(self, db: Session):
        self.db = db

    def top_genres(self, limit: int = 10) -> list[dict]:
        rows = (
            self.db.query(
                Genre.id.label("genre_id"),
                Genre.name,
                func.count(WatchHistory.id).label("activity_count"),
            )
            .join(Movie, Movie.genre_id == Genre.id)
            .outerjoin(WatchHistory, WatchHistory.movie_id == Movie.id)
            .group_by(Genre.id, Genre.name)
            .order_by(func.count(WatchHistory.id).desc(), Genre.name)
            .limit(limit)
            .all()
        )
        return [
            {"genre_id": row.genre_id, "name": row.name, "activity_count": row.activity_count}
            for row in rows
        ]

    def active_users(self, limit: int = 10) -> list[dict]:
        week_ago = datetime.utcnow() - timedelta(days=7)
        activities = union_all(
            select(Rating.user_id.label("user_id")).where(Rating.created_at >= week_ago),
            select(Watchlist.user_id.label("user_id")).where(Watchlist.added_at >= week_ago),
            select(WatchHistory.user_id.label("user_id")).where(WatchHistory.watched_at >= week_ago),
        ).subquery()
        rows = (
            self.db.query(
                User.id.label("user_id"),
                User.name,
                User.email,
                func.count(activities.c.user_id).label("activity_count"),
            )
            .join(activities, activities.c.user_id == User.id)
            .group_by(User.id, User.name, User.email)
            .order_by(func.count(activities.c.user_id).desc(), User.id)
            .limit(limit)
            .all()
        )
        return [
            {
                "user_id": row.user_id,
                "name": row.name,
                "email": row.email,
                "activity_count": row.activity_count,
            }
            for row in rows
        ]

    def most_watched(self, limit: int = 10) -> list[dict]:
        rows = (
            self.db.query(
                Movie.id.label("movie_id"),
                Movie.title,
                func.count(WatchHistory.id).label("watch_count"),
            )
            .outerjoin(WatchHistory, WatchHistory.movie_id == Movie.id)
            .group_by(Movie.id, Movie.title)
            .order_by(func.count(WatchHistory.id).desc(), Movie.title)
            .limit(limit)
            .all()
        )
        return [
            {"movie_id": row.movie_id, "title": row.title, "watch_count": row.watch_count}
            for row in rows
        ]

    def rating_distribution(self) -> list[dict]:
        rows = (
            self.db.query(Rating.rating, func.count(Rating.id).label("count"))
            .group_by(Rating.rating)
            .order_by(Rating.rating)
            .all()
        )
        return [{"rating": row.rating, "count": row.count} for row in rows]
