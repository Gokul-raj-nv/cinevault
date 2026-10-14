from typing import List, Optional
from sqlalchemy.orm import Session, joinedload

from app.models.movie import Movie
from app.models.watchlist import Watchlist


class WatchlistRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_item(self, user_id: int, movie_id: int) -> Optional[Watchlist]:
        return (
            self.db.query(Watchlist)
            .filter(Watchlist.user_id == user_id, Watchlist.movie_id == movie_id)
            .first()
        )

    def get_user_watchlist(self, user_id: int) -> List[Watchlist]:
        return (
            self.db.query(Watchlist)
            .options(joinedload(Watchlist.movie).joinedload(Movie.genre))
            .filter(Watchlist.user_id == user_id)
            .order_by(Watchlist.added_at.desc())
            .all()
        )

    def add(self, user_id: int, movie_id: int) -> Watchlist:
        item = Watchlist(user_id=user_id, movie_id=movie_id)
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def remove(self, item: Watchlist) -> None:
        self.db.delete(item)
        self.db.commit()

    def is_in_watchlist(self, user_id: int, movie_id: int) -> bool:
        return self.get_item(user_id, movie_id) is not None
