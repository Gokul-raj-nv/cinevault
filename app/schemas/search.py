from typing import List

from pydantic import BaseModel

from app.schemas.movie import MovieSummary


class MovieSearchResult(MovieSummary):
    """A movie result together with its semantic similarity score."""

    similarity: float


class SearchResponse(BaseModel):
    query: str
    results: List[MovieSearchResult]
