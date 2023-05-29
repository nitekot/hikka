from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
from app.database import get_session
from app.models import User
from app import constants
from typing import Tuple
from . import service

from .dependencies import (
    validate_activation_resend,
    validate_password_confirm,
    validate_password_reset,
    validate_activation,
    validate_signup,
    validate_login,
)

from .schemas import (
    TokenResponse,
    UserResponse,
    SignupArgs,
)


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/signup", response_model=UserResponse)
async def signup(
    signup: SignupArgs = Depends(validate_signup),
    session: AsyncSession = Depends(get_session),
):
    # Create new user
    user = await service.create_user(session, signup)

    # Add activation email to database
    await service.create_email(
        session,
        constants.EMAIL_ACTIVATION,
        user.activation_token,
        user,
    )

    return user


@router.post("/login", response_model=TokenResponse)
async def login(
    user: User = Depends(validate_login),
    session: AsyncSession = Depends(get_session),
):
    return await service.create_auth_token(session, user)


@router.post("/activation", response_model=UserResponse)
async def activation(
    user: User = Depends(validate_activation),
    session: AsyncSession = Depends(get_session),
):
    return await service.activate_user(session, user)


@router.post("/activation/resend", response_model=UserResponse)
async def activation_resend(
    user: User = Depends(validate_activation_resend),
    session: AsyncSession = Depends(get_session),
):
    user = await service.create_activation_token(session, user)

    # Add new activation email to database
    await service.create_email(
        session,
        constants.EMAIL_ACTIVATION,
        user.activation_token,
        user,
    )

    return user


@router.post("/password/reset", response_model=UserResponse)
async def reset_password(
    user: User = Depends(validate_password_reset),
    session: AsyncSession = Depends(get_session),
):
    user = await service.create_password_token(session, user)

    # Add new password reset email to database
    await service.create_email(
        session,
        constants.EMAIL_PASSWORD_RESET,
        user.password_reset_token,
        user,
    )

    return user


@router.post("/password/confirm", response_model=UserResponse)
async def password_reset(
    confirm: Tuple[User, str] = Depends(validate_password_confirm),
    session: AsyncSession = Depends(get_session),
):
    return await service.change_password(session, *confirm)