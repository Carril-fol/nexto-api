from dotenv import load_dotenv

from pydantic import EmailStr, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


load_dotenv()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    DATABASE_URL: str
    SECRET: str
    FRONTEND_URL: str

    MAIL_USERNAME: str
    MAIL_PASSWORD: SecretStr
    MAIL_FROM: EmailStr
    MAIL_SERVER: str
    MAIL_PORT: int = 587
    MAIL_STARTTLS: bool
    MAIL_SSL_TLS: bool

    COOKIE_SECURE: str

settings = Settings()