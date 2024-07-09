from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn, BaseModel
from functools import lru_cache
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(".env"))


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    DB_ECHO: bool  # Временно true;

    access_token_lifetime_seconds: int = 3600
    reset_password_token_secret: str
    verification_token_secret: str

    default_superuser_email: str
    default_superuser_password: str
    default_superuser_is_active: bool
    default_superuser_is_superuser: bool
    default_superuser_is_verified: bool

    @property
    def db_url(self) -> PostgresDsn:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    return settings
