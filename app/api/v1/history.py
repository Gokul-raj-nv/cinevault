from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.watch_history import WatchHistoryCreate, WatchHistoryResponse
from app.services.watch_history_service import WatchHistoryService

router = APIRouter(prefix="/history", tags=["Watch History"])


@router.get("", response_model=List[WatchHistoryResponse])
def get_watch_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get the current user's watch history, newest first."""
    return WatchHistoryService(db).get_history(current_user.id)


@router.post("/{movie_id}", status_code=status.HTTP_201_CREATED)
def log_watch(
    movie_id: int,
    data: WatchHistoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Log or update a watch event. POST /history/42 to log movie 42."""
    try:
        WatchHistoryService(db).log_watch(current_user.id, movie_id, data)
        return {"message": "Watch event logged"}
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
