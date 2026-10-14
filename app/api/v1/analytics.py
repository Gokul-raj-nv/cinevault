from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_admin
from app.db.session import get_db
from app.models.user import User
from app.schemas.analytics import (
    ActiveUserResponse,
    MostWatchedResponse,
    RatingDistributionResponse,
    TopGenreResponse,
)
from app.services.analytics_service import AnalyticsService

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/top-genres", response_model=List[TopGenreResponse])
def top_genres(
    limit: int = Query(default=10, ge=1, le=50),
    db: Session = Depends(get_db),
    _admin: User = Depends(get_current_admin),
):
    return AnalyticsService(db).top_genres(limit)


@router.get("/active-users", response_model=List[ActiveUserResponse])
def active_users(
    limit: int = Query(default=10, ge=1, le=50),
    db: Session = Depends(get_db),
    _admin: User = Depends(get_current_admin),
):
    return AnalyticsService(db).active_users(limit)


@router.get("/most-watched", response_model=List[MostWatchedResponse])
def most_watched(
    limit: int = Query(default=10, ge=1, le=50),
    db: Session = Depends(get_db),
    _admin: User = Depends(get_current_admin),
):
    return AnalyticsService(db).most_watched(limit)


@router.get("/average-ratings", response_model=List[RatingDistributionResponse])
def average_ratings(
    db: Session = Depends(get_db),
    _admin: User = Depends(get_current_admin),
):
    """Return the count of 1–5 star ratings."""
    return AnalyticsService(db).rating_distribution()
