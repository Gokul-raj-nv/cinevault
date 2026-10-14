from datetime import timedelta

from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import create_access_token, hash_password, verify_password
from app.repositories.user_repo import UserRepository
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse


class AuthService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    def register(self, data: RegisterRequest):
        """Register a new user. Raises ValueError if email already exists."""
        if self.repo.email_exists(data.email):
            raise ValueError("Email is already registered")

        password_hash = hash_password(data.password)
        user = self.repo.create(
            name=data.name,
            email=data.email,
            password_hash=password_hash,
        )
        return user

    def login(self, data: LoginRequest) -> TokenResponse:
        """Authenticate user and return JWT token. Raises ValueError on failure."""
        user = self.repo.get_by_email(data.email)

        if not user or not verify_password(data.password, user.password_hash):
            raise ValueError("Invalid email or password")

        if not user.is_active:
            raise ValueError("Account is deactivated")

        token = create_access_token(
            data={"sub": str(user.id)},
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        )

        return TokenResponse(access_token=token)