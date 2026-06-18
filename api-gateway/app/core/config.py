from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "api-gateway"
    APP_ENV: str = "development"

    AUTH_SERVICE_URL: str = "http://auth-service:8001"
    REDIS_URL : str
    RATE_LIMIT_ENABLED: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()