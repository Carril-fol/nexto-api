from dotenv import load_dotenv

from pydantic import EmailStr, SecretStr
from pydantic_settings import BaseSettings


load_dotenv()


class Settings(BaseSettings):
    DATABASE: str
    SECRET: str

    MAIL_USERNAME: str
    MAIL_PASSWORD: SecretStr
    MAIL_FROM: EmailStr
    MAIL_SERVER: str
    MAIL_PORT: int = 587

settings = Settings()