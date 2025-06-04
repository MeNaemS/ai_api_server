from fastapi import APIRouter, Request, HTTPException
from dishka.integrations.fastapi import DishkaRoute, FromDishka
from src.domain.models.user import AuthUser, RegisterUser
from src.infrastructure.dtos.token import Token
from src.application.usecases.auth_user_case import AuthService
from fastapi.security import OAuth2PasswordRequestForm  # ToDo: use it later


router = APIRouter(prefix="/auth", tags=["auth"], route_class=DishkaRoute)


@router.post("/token", response_model=Token)
async def login_for_access_token(
    request: Request,
    user: AuthUser,
    auth_service: FromDishka[AuthService]
):
    """Get access token for an existing user."""
    token = await auth_service.login_user(user)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return token


@router.post("/users", response_model=Token)
async def create_user(
    request: Request,
    user: RegisterUser,
    auth_service: FromDishka[AuthService]
):
    """Register a new user and get access token."""
    token = await auth_service.register_user(user)
    return token
