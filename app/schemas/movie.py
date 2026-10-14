from typing import List, Optional
from pydantic import BaseModel, Field
from app.schemas.genre import GenreResponse
from app.schemas.actor import ActorResponse


# --- Request schemas (what the client sends) ---

class MovieCreate(BaseModel):
    title: str
    description: Optional[str] = None
    release_year: Optional[int] = None
    runtime_minutes: Optional[int] = None
    language: str = "English"
    poster_url: Optional[str] = None
    genre_id: Optional[int] = None
    actor_ids: List[int] = Field(default_factory=list)  # IDs of actors to attach


class MovieUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    release_year: Optional[int] = None
    runtime_minutes: Optional[int] = None
    language: Optional[str] = None
    poster_url: Optional[str] = None
    genre_id: Optional[int] = None
    actor_ids: Optional[List[int]] = None


# --- Response schemas (what we return) ---

class MovieSummary(BaseModel):
    """Lightweight — used in lists."""
    id: int
    title: str
    release_year: Optional[int] = None
    runtime_minutes: Optional[int] = None
    language: str
    poster_url: Optional[str] = None
    genre: Optional[GenreResponse] = None

    model_config = {"from_attributes": True}


class MovieDetail(MovieSummary):
    """Full detail — used on single movie page."""
    description: Optional[str] = None
    actors: List[ActorResponse] = Field(default_factory=list)
    average_rating: Optional[float] = None

    model_config = {"from_attributes": True}


class PaginatedMovies(BaseModel):
    """Paginated list response."""
    total: int
    page: int
    page_size: int
    results: List[MovieSummary]
