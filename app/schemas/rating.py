from pydantic import BaseModel, Field
from typing import Optional


class RatingCreate(BaseModel):
    movie_id: int
    rating: int = Field(..., ge=1, le=5, description="Rating from 1 to 5")


class RatingResponse(BaseModel):
    id: int
    movie_id: int
    user_id: int
    rating: int

    model_config = {"from_attributes": True}


class MovieRatingSummary(BaseModel):
    movie_id: int
    average_rating: Optional[float]
    total_ratings: int