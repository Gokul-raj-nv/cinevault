from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_admin
from app.db.session import get_db
from app.models.user import User
from app.schemas.movie import MovieCreate, MovieDetail, MovieUpdate, MovieSummary, PaginatedMovies
from app.services.movie_service import MovieService

router = APIRouter(prefix="/movies", tags=["Movies"])


@router.get("", response_model=PaginatedMovies)
def list_movies(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    genre_id: Optional[int] = Query(default=None),
    search: Optional[str] = Query(default=None),
    language: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
):
    """Browse all movies with filters and pagination."""
    service = MovieService(db)
    total, movies = service.list_movies(
        page=page,
        page_size=page_size,
        genre_id=genre_id,
        search=search,
        language=language,
    )
    return PaginatedMovies(total=total, page=page, page_size=page_size, results=movies)


@router.get("/trending", response_model=List[MovieSummary])
def get_trending(db: Session = Depends(get_db)):
    """Get trending movies."""
    return MovieService(db).get_trending()


@router.get("/{movie_id}", response_model=MovieDetail)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    """Get full movie detail with actors and average rating."""
    try:
        return MovieService(db).get_movie(movie_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("", response_model=MovieDetail, status_code=201)
def create_movie(
    data: MovieCreate,
    db: Session = Depends(get_db),
    _admin: User = Depends(get_current_admin),
):
    """Create a movie. Admin only."""
    try:
        return MovieService(db).create_movie(data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/{movie_id}", response_model=MovieDetail)
def update_movie(
    movie_id: int,
    data: MovieUpdate,
    db: Session = Depends(get_db),
    _admin: User = Depends(get_current_admin),
):
    """Update a movie. Admin only."""
    try:
        return MovieService(db).update_movie(movie_id, data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{movie_id}", status_code=204)
def delete_movie(
    movie_id: int,
    db: Session = Depends(get_db),
    _admin: User = Depends(get_current_admin),
):
    """Delete a movie. Admin only."""
    try:
        MovieService(db).delete_movie(movie_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
