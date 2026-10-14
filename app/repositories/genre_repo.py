from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.genre import Genre


class GenreRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[Genre]:
        return self.db.query(Genre).order_by(Genre.name).all()

    def get_by_id(self, genre_id: int) -> Optional[Genre]:
        return self.db.query(Genre).filter(Genre.id == genre_id).first()

    def get_by_name(self, name: str) -> Optional[Genre]:
        return self.db.query(Genre).filter(Genre.name == name).first()

    def create(self, name: str) -> Genre:
        genre = Genre(name=name)
        self.db.add(genre)
        self.db.commit()
        self.db.refresh(genre)
        return genre