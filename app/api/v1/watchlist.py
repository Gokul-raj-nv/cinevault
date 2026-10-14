from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.watchlist import WatchlistResponse, WatchlistStatusResponse
from app.services.watchlist_service import WatchlistService

router = APIRouter(prefix="/watchlist", tags=["Watchlist"])


@router.get("", response_model=List[WatchlistResponse])
def get_watchlist(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get all movies in the current user's watchlist."""
    return WatchlistService(db).get_watchlist(current_user.id)


@router.post("/{movie_id}", status_code=201)
def add_to_watchlist(
    movie_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Add a movie to watchlist."""
    try:
        WatchlistService(db).add_to_watchlist(current_user.id, movie_id)
        return {"message": "Added to watchlist"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{movie_id}", status_code=200)
def remove_from_watchlist(
    movie_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Remove a movie from watchlist."""
    try:
        WatchlistService(db).remove_from_watchlist(current_user.id, movie_id)
        return {"message": "Removed from watchlist"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/status/{movie_id}", response_model=WatchlistStatusResponse)
def check_watchlist_status(
    movie_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Check if a movie is in the user's watchlist."""
    return WatchlistService(db).check_status(current_user.id, movie_id)