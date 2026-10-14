from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from app.schemas.movie import MovieSummary


class WatchHistoryCreate(BaseModel):
    last_position_seconds: Optional[int] = Field(default=0, ge=0)


class WatchHistoryResponse(BaseModel):
    id: int
    movie_id: int
    watched_at: datetime
    last_position_seconds: int
    movie: MovieSummary

    model_config = {"from_attributes": True}
