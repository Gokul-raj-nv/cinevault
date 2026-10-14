from functools import lru_cache
from typing import Any

from sqlalchemy.orm import Session, joinedload

from app.core.config import settings
from app.models.movie import Movie
from app.repositories.movie_repo import MovieRepository
from app.services.movie_presenter import movie_summary_payload


@lru_cache(maxsize=1)
def _embedding_model() -> Any:
    """Load the transformer once per API process, not once per request."""
    # Import lazily: starting ordinary CRUD routes must not load the ML runtime.
    from sentence_transformers import SentenceTransformer

    return SentenceTransformer(settings.EMBEDDING_MODEL)


class SearchService:
    def __init__(self, db: Session):
        self.db = db
        self.movie_repo = MovieRepository(db)

    @staticmethod
    def _movie_text(movie: Movie) -> str:
        genre_name = movie.genre.name if movie.genre is not None else ""
        return "\n".join(part for part in (movie.title, genre_name, movie.description or "") if part)

    @staticmethod
    def _embed(text: str) -> list[float]:
        embedding = _embedding_model().encode(text, normalize_embeddings=True)
        return embedding.tolist()

    def index_movie(self, movie: Movie) -> None:
        """Generate and persist the vector used by semantic search."""
        movie.embedding = self._embed(self._movie_text(movie))
        self.db.commit()
        self.db.refresh(movie)

    def reindex_all_movies(self) -> int:
        movies = self.db.query(Movie).options(joinedload(Movie.genre)).all()
        for movie in movies:
            self.index_movie(movie)
        return len(movies)

    def search(self, query: str, limit: int) -> list[dict]:
        if not settings.SEMANTIC_SEARCH_ENABLED:
            raise RuntimeError("Semantic search is disabled")
        query_embedding = self._embed(query)
        rows = self.movie_repo.search_by_embedding(query_embedding, limit)
        results: list[dict] = []
        for movie, distance in rows:
            payload = movie_summary_payload(movie)
            # Cosine distance is 0 for an identical vector and can approach 2.
            payload["similarity"] = round(max(0.0, min(1.0, 1.0 - distance)), 4)
            results.append(payload)
        return results
