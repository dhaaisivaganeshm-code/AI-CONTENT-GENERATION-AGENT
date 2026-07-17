from functools import cached_property

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration."""

    # ==========================
    # MongoDB
    # ==========================
    mongodb_url: str = Field(default="mongodb://localhost:27017")
    mongodb_db: str = Field(default="ai_content_assistant")

    # ==========================
    # JWT
    # ==========================
    jwt_secret: str
    jwt_algorithm: str = Field(default="HS256")
    access_token_expire_minutes: int = Field(default=1440)

    # ==========================
    # AI
    # ==========================
    ai_provider: str = Field(default="groq")
    ai_api_key: str = Field(default="")
    ai_model: str = Field(default="llama-3.3-70b-versatile")

    # ==========================
    # CORS
    # ==========================
    cors_origins: str = Field(
        default="http://localhost:5500,http://127.0.0.1:5500"
    )

    @cached_property
    def cors_origin_list(self):
        return [origin.strip() for origin in self.cors_origins.split(",")]

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()