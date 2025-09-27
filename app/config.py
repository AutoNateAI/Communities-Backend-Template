from functools import lru_cache
from typing import Literal

from pydantic import AnyUrl, BaseSettings, Field


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    app_name: str = Field(default="Communities Backend Template")
    app_env: Literal["local", "production"] = Field(default="local", env="APP_ENV")
    database_url_local: AnyUrl | str = Field(..., env="DATABASE_URL_LOCAL")
    database_url_prod: AnyUrl | str = Field(..., env="DATABASE_URL_PROD")
    jwt_secret_key: str = Field(..., env="JWT_SECRET_KEY")
    jwt_algorithm: str = Field(default="HS256", env="JWT_ALGORITHM")
    access_token_expire_minutes: int = Field(default=60, env="ACCESS_TOKEN_EXPIRE_MINUTES")

    class Config:
        env_file = ".env"
        case_sensitive = False

    @property
    def database_url(self) -> str:
        """Return the database URL for the configured environment."""

        if self.app_env == "production":
            return str(self.database_url_prod)
        return str(self.database_url_local)


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings."""

    return Settings()
