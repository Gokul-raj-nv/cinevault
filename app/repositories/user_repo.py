from typing import Optional

from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str) -> Optional[User]:
        """Find a user by their email address."""
        return self.db.query(User).filter(User.email == email).first()

    def get_by_id(self, user_id: int) -> Optional[User]:
        """Find a user by their ID."""
        return self.db.query(User).filter(User.id == user_id).first()

    def create(self, name: str, email: str, password_hash: str) -> User:
        """Create and save a new user."""
        user = User(name=name, email=email, password_hash=password_hash)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def email_exists(self, email: str) -> bool:
        """Check if an email is already registered."""
        return self.db.query(User).filter(User.email == email).count() > 0