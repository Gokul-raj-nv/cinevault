from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.rating import MovieRatingSummary, RatingCreate, RatingResponse
from app.services.rating_service import RatingService

router = APIRouter(prefix="/ratings", tags=["Ratings"])


@router.post("", response_model=RatingResponse, status_code=201)
def rate_movie(
    data: RatingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Rate a movie (1–5 stars). Updates existing rating if already rated."""
    try:
        return RatingService(db).rate_movie(user_id=current_user.id, data=data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/movie/{movie_id}", response_model=MovieRatingSummary)
def get_movie_rating_stats(movie_id: int, db: Session = Depends(get_db)):
    """Get average rating and total count for a movie."""
    try:
        return RatingService(db).get_movie_stats(movie_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/my/{movie_id}", response_model=RatingResponse)
def get_my_rating(
    movie_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get the current user's rating for a specific movie."""
    rating = RatingService(db).get_my_rating(current_user.id, movie_id)
    if not rating:
        raise HTTPException(status_code=404, detail="You haven't rated this movie yet")
    return rating