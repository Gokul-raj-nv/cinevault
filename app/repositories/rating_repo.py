from typing import List, Optional
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.rating import Rating


class RatingRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_rating(self, user_id: int, movie_id: int) -> Optional[Rating]:
        return (
            self.db.query(Rating)
            .filter(Rating.user_id == user_id, Rating.movie_id == movie_id)
            .first()
        )

    def upsert(self, user_id: int, movie_id: int, rating: int) -> Rating:
        """Create rating or update if already exists."""
        existing = self.get_user_rating(user_id, movie_id)
        if existing:
            existing.rating = rating
            self.db.commit()
            self.db.refresh(existing)
            return existing

        new_rating = Rating(user_id=user_id, movie_id=movie_id, rating=rating)
        self.db.add(new_rating)
        self.db.commit()
        self.db.refresh(new_rating)
        return new_rating

    def get_movie_stats(self, movie_id: int) -> dict:
        result = (
            self.db.query(
                func.avg(Rating.rating).label("average"),
                func.count(Rating.id).label("total"),
            )
            .filter(Rating.movie_id == movie_id)
            .first()
        )
        return {
            "average_rating": round(float(result.average), 2) if result.average else None,
            "total_ratings": result.total or 0,
        }