from functools import lru_cache
from typing import Literal

from pydantic import AnyUrl, Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    app_name: str = Field(default="Communities Backend Template")
    app_env: Literal["local", "production"] = Field(default="local", env="APP_ENV")
    database_url_local: AnyUrl | str = Field(..., env="DATABASE_URL_LOCAL")
    database_url_prod: AnyUrl | str = Field(..., env="DATABASE_URL_PROD")
    jwt_secret_key: str = Field(..., env="JWT_SECRET_KEY")
    jwt_algorithm: str = Field(default="HS256", env="JWT_ALGORITHM")
    access_token_expire_minutes: int = Field(default=60, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    cors_origin_local: str = Field(default="http://127.0.0.1:5500", env="CORS_ORIGIN_LOCAL")
    cors_origin_prod: str = Field(
        default="https://backend-template-small-snowflake-3911.fly.dev",
        env="CORS_ORIGIN_PROD",
    )

    class Config:
        env_file = ".env"
        case_sensitive = False

    @staticmethod
    def _trim_trailing_slash(value: str) -> str:
        """Return the origin without a trailing slash to satisfy CORS checks."""

        return value[:-1] if value.endswith("/") else value

    @property
    def database_url(self) -> str:
        """Return the database URL for the configured environment."""

        if self.app_env == "production":
            return str(self.database_url_prod)
        return str(self.database_url_local)

    @property
    def cors_origins(self) -> list[str]:
        """Return the allowed CORS origins for the current environment."""

        origin = self.cors_origin_prod if self.app_env == "production" else self.cors_origin_local
        return [self._trim_trailing_slash(origin)]


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings."""

    return Settings()
