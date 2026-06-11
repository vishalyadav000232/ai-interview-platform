from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRATE_KEY :str = 'D'
    JWT_ALGORITHM :str = 'HS256'
    REFRESH_TOKEN_EXPIRE_MINUTS : int = 30
    REFRESH_TOKEN_EXPIRE_DAYS : int = 7

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()