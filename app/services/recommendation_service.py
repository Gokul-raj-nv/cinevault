from collections import defaultdict

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.cache import get_json, set_json
from app.core.config import settings
from app.models.movie import Movie
from app.models.rating import Rating
from app.models.watch_history import WatchHistory
from app.models.watchlist import Watchlist
from app.repositories.movie_repo import MovieRepository
from app.services.movie_presenter import movie_summary_payload


class RecommendationService:
    """A transparent, genre-weighted recommender that can later be replaced by ML."""

    def __init__(self, db: Session):
        self.db = db
        self.movie_repo = MovieRepository(db)

    def get_recommendations(self, user_id: int, limit: int = 10) -> list[dict]:
        cache_key = f"recommendations:{user_id}"
        cached = get_json(cache_key)
        if cached is not None:
            return cached

        genre_weights = self._genre_weights(user_id)
        if not genre_weights:
            results = [movie_summary_payload(movie) for movie in self.movie_repo.get_trending(limit)]
            set_json(cache_key, results, settings.RECOMMENDATIONS_CACHE_TTL_SECONDS)
            return results

        watched_ids = [
            movie_id
            for (movie_id,) in self.db.query(WatchHistory.movie_id)
            .filter(WatchHistory.user_id == user_id)
            .all()
        ]
        query = (
            self.db.query(
                Movie,
                func.coalesce(func.avg(Rating.rating), 0).label("average_rating"),
            )
            .outerjoin(Rating, Rating.movie_id == Movie.id)
            .filter(Movie.genre_id.in_(genre_weights.keys()))
        )
        if watched_ids:
            query = query.filter(~Movie.id.in_(watched_ids))

        candidates = query.group_by(Movie.id).all()
        candidates.sort(
            key=lambda row: (
                genre_weights.get(row.Movie.genre_id, 0.0),
                float(row.average_rating),
                row.Movie.created_at,
            ),
            reverse=True,
        )
        results = [movie_summary_payload(row.Movie) for row in candidates[:limit]]
        set_json(cache_key, results, settings.RECOMMENDATIONS_CACHE_TTL_SECONDS)
        return results

    def _genre_weights(self, user_id: int) -> dict[int, float]:
        weights: defaultdict[int, float] = defaultdict(float)

        # A highly rated movie influences the result more than a low-rated one.
        rated = (
            self.db.query(Movie.genre_id, func.sum(Rating.rating))
            .join(Rating, Rating.movie_id == Movie.id)
            .filter(Rating.user_id == user_id, Movie.genre_id.is_not(None))
            .group_by(Movie.genre_id)
            .all()
        )
        for genre_id, weight in rated:
            weights[genre_id] += float(weight)

        history = (
            self.db.query(Movie.genre_id, func.count(WatchHistory.id))
            .join(WatchHistory, WatchHistory.movie_id == Movie.id)
            .filter(WatchHistory.user_id == user_id, Movie.genre_id.is_not(None))
            .group_by(Movie.genre_id)
            .all()
        )
        for genre_id, count in history:
            weights[genre_id] += float(count)

        watchlist = (
            self.db.query(Movie.genre_id, func.count(Watchlist.id))
            .join(Watchlist, Watchlist.movie_id == Movie.id)
            .filter(Watchlist.user_id == user_id, Movie.genre_id.is_not(None))
            .group_by(Movie.genre_id)
            .all()
        )
        for genre_id, count in watchlist:
            weights[genre_id] += float(count)

        return dict(weights)
