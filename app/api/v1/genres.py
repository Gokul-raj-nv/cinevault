from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.dependencies import get_current_admin
from app.db.session import get_db
from app.models.user import User
from app.schemas.genre import GenreCreate, GenreResponse
from app.services.genre_service import GenreService

router = APIRouter(prefix="/genres", tags=["Genres"])


@router.get("", response_model=List[GenreResponse])
def list_genres(db: Session = Depends(get_db)):
    """Get all genres."""
    return GenreService(db).list_genres()


@router.post("", response_model=GenreResponse, status_code=201)
def create_genre(
    data: GenreCreate,
    db: Session = Depends(get_db),
    _admin: User = Depends(get_current_admin),
):
    """Create a genre. Admin only."""
    try:
        return GenreService(db).create_genre(data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))