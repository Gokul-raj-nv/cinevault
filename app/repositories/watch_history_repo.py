from typing import List, Optional
from sqlalchemy.orm import Session, joinedload

from app.models.movie import Movie
from app.models.watch_history import WatchHistory


class WatchHistoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_entry(self, user_id: int, movie_id: int) -> Optional[WatchHistory]:
        return (
            self.db.query(WatchHistory)
            .filter(
                WatchHistory.user_id == user_id,
                WatchHistory.movie_id == movie_id,
            )
            .first()
        )

    def get_user_history(self, user_id: int, limit: int = 20) -> List[WatchHistory]:
        return (
            self.db.query(WatchHistory)
            .options(joinedload(WatchHistory.movie).joinedload(Movie.genre))
            .filter(WatchHistory.user_id == user_id)
            .order_by(WatchHistory.watched_at.desc())
            .limit(limit)
            .all()
        )

    def upsert(self, user_id: int, movie_id: int, position: int = 0) -> WatchHistory:
        """Log a watch event — update if already exists (continue watching)."""
        from datetime import datetime
        existing = self.get_entry(user_id, movie_id)
        if existing:
            existing.last_position_seconds = position
            existing.watched_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(existing)
            return existing

        entry = WatchHistory(
            user_id=user_id,
            movie_id=movie_id,
            last_position_seconds=position,
        )
        self.db.add(entry)
        self.db.commit()
        self.db.refresh(entry)
        return entry
