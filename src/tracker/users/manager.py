import uuid
import re
from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, UUIDIDMixin, InvalidPasswordException
from fastapi_users.db import SQLAlchemyUserDatabase

from tracker.shared.core.database import get_async_db
from tracker.shared.core.config import settings
from tracker.shared.infrastructure.mail import send_email

from tracker.users.models import User


PASSWORD_REGEX = re.compile(
    r"^(?=.*\d)"
    r"(?=.*[a-z])"
    r"(?=.*[A-Z])"
    r"(?=.*[^A-Za-z0-9\s])"
    r"\S{8,128}$"
)

class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = settings.SECRET
    verification_token_secret = settings.SECRET

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        link = f"{settings.FRONTEND_URL}/reset-password?token={token}"
        await send_email(
            subject="Recuperá tu contraseña",
            recipients=[user.email],
            body=f"<p>Hacé click <a href='{link}'>acá</a> para cambiar tu contraseña.</p>",
        )

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        await self.request_verify(user, request)

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        link = f"{settings.FRONTEND_URL}/verify-email?token={token}"
        await send_email(
            subject="Verificá tu email",
            recipients=[user.email],
            body=(
                f"<p>Hola {user.first_name}, hacé click "
                f"<a href='{link}'>acá</a> para verificar tu cuenta.</p>"
            ),
    )

    async def validate_password(self, password: str, user) -> None:
        """
        Validate password using regex.
        
        The function receives the password and the user instance, 
        which is using regex compares the user's instructions with the password to see if it meets the requirements
        """
        if not PASSWORD_REGEX.match(password):
            raise InvalidPasswordException(
                reason=(
                    "The password must be between 8 and 128 characters, with no spaces,"
                    "and include a number, a lowercase letter, a capital letter and a special character"
                )
            )
        if user.email in password:
            raise InvalidPasswordException(
                reason="The passoword can´t contain a email"
            )


async def get_user_db(session=Depends(get_async_db)):
    yield SQLAlchemyUserDatabase(session, User)


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)