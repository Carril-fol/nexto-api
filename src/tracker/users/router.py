from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_users import exceptions
from fastapi_users.authentication import Strategy

from tracker.users.auth import auth_backend, fastapi_users
from tracker.users.manager import UserManager, get_user_manager
from tracker.users.models import User
from tracker.users.schema import UserCreate, UserRead, UserUpdate, LoginRequest, RegisterRequest

router = APIRouter()


get_current_user_token = fastapi_users.authenticator.current_user_token(
    active=True, verified=True
)


@router.post(
    "/auth/register",
    tags=["auth"],
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    request: Request,
    data: RegisterRequest,
    user_manager: UserManager = Depends(get_user_manager),
):
    user_create = UserCreate(
        first_name=data.first_name,
        last_name=data.last_name,
        email=data.email,
        password=data.password,
    )

    try:
        user = await user_manager.create(user_create, safe=True, request=request)
    except exceptions.UserAlreadyExists:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "REGISTER_USER_ALREADY_EXISTS")
    except exceptions.InvalidPasswordException as e:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail={"code": "REGISTER_INVALID_PASSWORD", "reason": e.reason},
        )

    return user


@router.post("/auth/login", tags=["auth"], status_code=status.HTTP_200_OK)
async def login(
    request: Request,
    data: LoginRequest,
    user_manager: UserManager = Depends(get_user_manager),
    strategy: Strategy = Depends(auth_backend.get_strategy),
):
    credentials = OAuth2PasswordRequestForm(username=data.email, password=data.password
)
    user = await user_manager.authenticate(credentials)

    if user is None or not user.is_active:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "LOGIN_BAD_CREDENTIALS")
    if not user.is_verified:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "LOGIN_USER_NOT_VERIFIED")

    response = await auth_backend.login(strategy, user)
    await user_manager.on_after_login(user, request, response)
    return response


@router.get("/verify-email", tags=["auth"])
async def verify_email(
    token: str,
    user_manager: UserManager = Depends(get_user_manager),
):
    try:
        await user_manager.verify(token)
    except exceptions.InvalidVerifyToken:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "VERIFY_USER_BAD_TOKEN")
    except exceptions.UserAlreadyVerified:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "VERIFY_USER_ALREADY_VERIFIED")

    return {"detail": "Email verificado correctamente"}


@router.post("/auth/logout", tags=["auth"], status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    user_token: tuple[User, str] = Depends(get_current_user_token),
    strategy: Strategy = Depends(auth_backend.get_strategy),
):
    user, token = user_token
    return await auth_backend.logout(strategy, user, token)


router.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth", tags=["auth"],
)
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users", tags=["users"],
)