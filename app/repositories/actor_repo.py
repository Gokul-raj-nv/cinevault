from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.actor import Actor


class ActorRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, actor_id: int) -> Optional[Actor]:
        return self.db.query(Actor).filter(Actor.id == actor_id).first()

    def get_by_ids(self, actor_ids: List[int]) -> List[Actor]:
        return self.db.query(Actor).filter(Actor.id.in_(actor_ids)).all()

    def get_all(self) -> List[Actor]:
        return self.db.query(Actor).order_by(Actor.name).all()

    def create(self, name: str, bio: Optional[str] = None) -> Actor:
        actor = Actor(name=name, bio=bio)
        self.db.add(actor)
        self.db.commit()
        self.db.refresh(actor)
        return actor