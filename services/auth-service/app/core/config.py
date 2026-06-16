from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    TEST_DATABASE_URL: str | None = None
    JWT_SECRATE_KEY :str = 'D'
    JWT_ALGORITHM :str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTS : int = 30
    REFRESH_TOKEN_EXPIRE_DAYS : int = 7
    RESEND_API_KEY: str
    EMAIL_FROM: str = "AI Interview <onboarding@resend.dev>"
    AUTH_SERVICE_BASE_URL:str
    REDIS_URL: str = "redis://redis:6379/0"
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()