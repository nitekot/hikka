from app.dependencies import auth_required, get_user
from .schemas import UserResponse, DescriptionArgs
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
from app.database import get_session
from app.models import User
from . import service


router = APIRouter(prefix="/user", tags=["User"])


@router.get("/me", response_model=UserResponse)
async def profile(user: User = Depends(auth_required)):
    return user


@router.get("/{username}", response_model=UserResponse)
async def user_profile(user: User = Depends(get_user)):
    return user


# ToDo: move to user settings
@router.post("/description", response_model=UserResponse)
async def change_description(
    args: DescriptionArgs,
    user: User = Depends(auth_required),
    session: AsyncSession = Depends(get_session),
):
    return await service.change_description(session, user, args.description)