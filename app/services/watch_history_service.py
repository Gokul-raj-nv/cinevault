from sqlalchemy.orm import Session

from app.core.cache import delete as cache_delete
from app.repositories.movie_repo import MovieRepository
from app.repositories.watch_history_repo import WatchHistoryRepository
from app.schemas.watch_history import WatchHistoryCreate


class WatchHistoryService:
    def __init__(self, db: Session):
        self.repo = WatchHistoryRepository(db)
        self.movie_repo = MovieRepository(db)

    def log_watch(self, user_id: int, movie_id: int, data: WatchHistoryCreate):
        movie = self.movie_repo.get_by_id(movie_id)
        if not movie:
            raise ValueError(f"Movie {movie_id} not found")

        entry = self.repo.upsert(
            user_id=user_id,
            movie_id=movie_id,
            position=data.last_position_seconds or 0,
        )
        cache_delete(f"recommendations:{user_id}")
        return entry

    def get_history(self, user_id: int):
        return self.repo.get_user_history(user_id)
