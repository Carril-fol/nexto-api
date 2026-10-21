import uuid

from fastapi_users import FastAPIUsers
from fastapi_users.authentication import (
    AuthenticationBackend,
    CookieTransport,
    JWTStrategy,
)

from tracker.shared.core.config import settings
from tracker.users.manager import get_user_manager
from tracker.users.models import User

SESSION_SECONDS = 60 * 60 * 24 * 7  # 7 días

cookie_transport = CookieTransport(
    cookie_name="tracker_auth",
    cookie_max_age=SESSION_SECONDS,
    cookie_secure=settings.COOKIE_SECURE,
    cookie_httponly=True,
    cookie_samesite="lax",
)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.SECRET, lifetime_seconds=SESSION_SECONDS)


auth_backend = AuthenticationBackend(
    name="cookie",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])

current_active_user = fastapi_users.current_user(active=True)
current_verified_user = fastapi_users.current_user(active=True, verified=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)