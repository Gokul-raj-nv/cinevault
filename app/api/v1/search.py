from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_admin
from app.db.session import get_db
from app.models.user import User
from app.schemas.search import SearchResponse
from app.services.search_service import SearchService

router = APIRouter(prefix="/search", tags=["Semantic Search"])


@router.get("", response_model=SearchResponse)
def search_movies(
    q: str = Query(..., min_length=2, max_length=500, description="Natural-language movie query"),
    limit: int = Query(default=10, ge=1, le=50),
    db: Session = Depends(get_db),
):
    """Find movies by meaning, not just title keyword matching."""
    try:
        results = SearchService(db).search(q, limit)
        return {"query": q, "results": results}
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Semantic search is unavailable. Confirm PostgreSQL pgvector is running and the model can download.",
        ) from exc


@router.post("/reindex", status_code=status.HTTP_202_ACCEPTED)
def reindex_movies(
    db: Session = Depends(get_db),
    _admin: User = Depends(get_current_admin),
):
    """Create embeddings for movies that existed before semantic search was added."""
    try:
        indexed = SearchService(db).reindex_all_movies()
        return {"message": "Semantic search index updated", "indexed_movies": indexed}
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Could not build embeddings. Check the model download and pgvector setup.",
        ) from exc
