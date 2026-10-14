from pydantic import BaseModel
from typing import Optional


class ActorBase(BaseModel):
    name: str
    bio: Optional[str] = None


class ActorCreate(ActorBase):
    pass


class ActorResponse(ActorBase):
    id: int

    model_config = {"from_attributes": True}