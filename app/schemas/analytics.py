from pydantic import BaseModel


class TopGenreResponse(BaseModel):
    genre_id: int
    name: str
    activity_count: int


class ActiveUserResponse(BaseModel):
    user_id: int
    name: str
    email: str
    activity_count: int


class MostWatchedResponse(BaseModel):
    movie_id: int
    title: str
    watch_count: int


class RatingDistributionResponse(BaseModel):
    rating: int
    count: int
