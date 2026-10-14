from datetime import datetime
from pydantic import BaseModel
from app.schemas.movie import MovieSummary


class WatchlistResponse(BaseModel):
    id: int
    movie_id: int
    added_at: datetime
    movie: MovieSummary

    model_config = {"from_attributes": True}


class WatchlistStatusResponse(BaseModel):
    movie_id: int
    in_watchlist: bool