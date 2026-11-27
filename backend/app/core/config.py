from functools import lru_cache

from pydantic import AnyUrl, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "SignalDesk AI"
    environment: str = "development"
    api_v1_prefix: str = "/api/v1"
    secret_key: str = Field(default="dev-secret", min_length=8)
    access_token_expire_minutes: int = 1440
    database_url: str = "postgresql+asyncpg://postgres:postgres@postgres:5432/whatsapp_ai"
    redis_url: str = "redis://redis:6379/0"
    cors_origins: str = "http://localhost:5173,http://localhost:3000"

    openai_api_key: str | None = None
    openai_model: str = "gpt-5"

    whatsapp_phone_number_id: str | None = None
    whatsapp_business_account_id: str | None = None
    whatsapp_access_token: str | None = None
    whatsapp_verify_token: str = "local-verify-token"
    public_webhook_url: AnyUrl | str = "http://localhost:8000/api/v1/whatsapp/webhook"

    jwt_algorithm: str = "HS256"

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
