from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.core.dependencies import get_current_admin
from app.db.session import get_db
from app.models.user import User
from app.schemas.actor import ActorCreate, ActorResponse
from app.repositories.actor_repo import ActorRepository

router = APIRouter(prefix="/actors", tags=["Actors"])


@router.get("", response_model=List[ActorResponse])
def list_actors(db: Session = Depends(get_db)):
    return ActorRepository(db).get_all()


@router.post("", response_model=ActorResponse, status_code=201)
def create_actor(
    data: ActorCreate,
    db: Session = Depends(get_db),
    _admin: User = Depends(get_current_admin),
):
    return ActorRepository(db).create(name=data.name, bio=data.bio)