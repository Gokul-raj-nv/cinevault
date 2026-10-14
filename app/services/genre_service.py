from sqlalchemy.orm import Session

from app.core.cache import delete as cache_delete
from app.core.cache import get_json, set_json
from app.core.config import settings
from app.repositories.genre_repo import GenreRepository
from app.schemas.genre import GenreCreate, GenreResponse


class GenreService:
    def __init__(self, db: Session):
        self.repo = GenreRepository(db)

    def list_genres(self):
        cache_key = "genres:all"
        cached = get_json(cache_key)
        if cached is not None:
            return cached

        genres = self.repo.get_all()
        payload = [GenreResponse.model_validate(genre).model_dump(mode="json") for genre in genres]
        set_json(cache_key, payload, settings.GENRES_CACHE_TTL_SECONDS)
        return genres

    def create_genre(self, data: GenreCreate):
        if self.repo.get_by_name(data.name) is not None:
            raise ValueError("A genre with this name already exists")
        genre = self.repo.create(data.name)
        cache_delete("genres:all")
        return genre
