"""Convert ORM movies into JSON-safe response dictionaries for Redis."""

from app.models.movie import Movie
from app.schemas.movie import MovieDetail, MovieSummary


def movie_summary_payload(movie: Movie) -> dict:
    return MovieSummary.model_validate(movie).model_dump(mode="json")


def movie_detail_payload(movie: Movie) -> dict:
    return MovieDetail.model_validate(movie).model_dump(mode="json")
