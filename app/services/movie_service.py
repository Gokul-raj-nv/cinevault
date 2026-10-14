import logging
from typing import Optional

from sqlalchemy.orm import Session

from app.core.cache import delete as cache_delete
from app.core.cache import get_json, set_json
from app.core.config import settings
from app.repositories.actor_repo import ActorRepository
from app.repositories.genre_repo import GenreRepository
from app.repositories.movie_repo import MovieRepository
from app.schemas.movie import MovieCreate, MovieUpdate
from app.services.movie_presenter import movie_detail_payload, movie_summary_payload

logger = logging.getLogger(__name__)


class MovieService:
    def __init__(self, db: Session):
        self.db = db
        self.movie_repo = MovieRepository(db)
        self.genre_repo = GenreRepository(db)
        self.actor_repo = ActorRepository(db)

    @staticmethod
    def _movie_cache_key(movie_id: int) -> str:
        return f"movies:{movie_id}"

    def _invalidate_movie_caches(self, movie_id: int) -> None:
        cache_delete(self._movie_cache_key(movie_id), "movies:trending")

    def _index_movie(self, movie) -> None:
        """Indexing is useful but must not make ordinary CRUD unavailable."""
        if not settings.SEMANTIC_SEARCH_ENABLED:
            return
        try:
            from app.services.search_service import SearchService

            SearchService(self.db).index_movie(movie)
        except Exception:
            self.db.rollback()
            logger.exception("Could not create the semantic-search embedding for movie %s", movie.id)

    def list_movies(
        self,
        page: int = 1,
        page_size: int = 20,
        genre_id: Optional[int] = None,
        search: Optional[str] = None,
        language: Optional[str] = None,
    ):
        return self.movie_repo.get_all(
            page=page,
            page_size=page_size,
            genre_id=genre_id,
            search=search,
            language=language,
        )

    def get_movie(self, movie_id: int):
        cache_key = self._movie_cache_key(movie_id)
        cached = get_json(cache_key)
        if cached is not None:
            return cached

        movie = self.movie_repo.get_by_id(movie_id)
        if movie is None:
            raise ValueError(f"Movie with id {movie_id} not found")

        movie.average_rating = self.movie_repo.get_average_rating(movie_id)
        set_json(cache_key, movie_detail_payload(movie), settings.MOVIE_CACHE_TTL_SECONDS)
        return movie

    def create_movie(self, data: MovieCreate):
        if data.genre_id is not None and self.genre_repo.get_by_id(data.genre_id) is None:
            raise ValueError(f"Genre with id {data.genre_id} not found")

        actors = self._validated_actors(data.actor_ids)
        movie = self.movie_repo.create(**data.model_dump(exclude={"actor_ids"}))
        movie.actors = actors
        self.movie_repo.update(movie)
        self._index_movie(movie)
        self._invalidate_movie_caches(movie.id)
        return self.get_movie(movie.id)

    def update_movie(self, movie_id: int, data: MovieUpdate):
        movie = self.movie_repo.get_by_id(movie_id)
        if movie is None:
            raise ValueError(f"Movie with id {movie_id} not found")

        update_data = data.model_dump(exclude_unset=True)
        if "genre_id" in update_data and update_data["genre_id"] is not None:
            if self.genre_repo.get_by_id(update_data["genre_id"]) is None:
                raise ValueError(f"Genre with id {update_data['genre_id']} not found")

        actor_ids = update_data.pop("actor_ids", None)
        if actor_ids is not None:
            movie.actors = self._validated_actors(actor_ids)

        self.movie_repo.update(movie, **update_data)
        if {"title", "description", "genre_id"}.intersection(update_data) or actor_ids is not None:
            self._index_movie(movie)
        self._invalidate_movie_caches(movie.id)
        return self.get_movie(movie.id)

    def delete_movie(self, movie_id: int) -> None:
        movie = self.movie_repo.get_by_id(movie_id)
        if movie is None:
            raise ValueError(f"Movie with id {movie_id} not found")
        self.movie_repo.delete(movie)
        self._invalidate_movie_caches(movie_id)

    def get_trending(self):
        cache_key = "movies:trending"
        cached = get_json(cache_key)
        if cached is not None:
            return cached

        movies = self.movie_repo.get_trending()
        set_json(
            cache_key,
            [movie_summary_payload(movie) for movie in movies],
            settings.TRENDING_CACHE_TTL_SECONDS,
        )
        return movies

    def _validated_actors(self, actor_ids: list[int]):
        if len(actor_ids) != len(set(actor_ids)):
            raise ValueError("Actor IDs must not contain duplicates")
        actors = self.actor_repo.get_by_ids(actor_ids)
        if len(actors) != len(actor_ids):
            raise ValueError("One or more actor IDs are invalid")
        return actors
