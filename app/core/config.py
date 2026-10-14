from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from the local .env file."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    REDIS_URL: str = "redis://localhost:6379/0"
    CACHE_ENABLED: bool = True
    TRENDING_CACHE_TTL_SECONDS: int = 300
    GENRES_CACHE_TTL_SECONDS: int = 3600
    MOVIE_CACHE_TTL_SECONDS: int = 600
    RECOMMENDATIONS_CACHE_TTL_SECONDS: int = 900

    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    EMBEDDING_DIMENSION: int = 384
    SEMANTIC_SEARCH_ENABLED: bool = True


settings = Settings()
