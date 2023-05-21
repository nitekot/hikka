from .schemas import WatchPaginationResponse, WatchFilterArgs
from app.utils import pagination, pagination_dict
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_user, get_page
from fastapi import APIRouter, Depends
from app.database import get_session
from app.models import User
from . import service


router = APIRouter(prefix="/list", tags=["List"])


@router.get("/{username}/anime", response_model=WatchPaginationResponse)
async def anime_list(
    session: AsyncSession = Depends(get_session),
    filter: WatchFilterArgs = Depends(),
    user: User = Depends(get_user),
    page: int = Depends(get_page),
):
    total = await service.get_user_watch_count(session, user, filter.status)
    limit, offset = pagination(page)
    result = await service.get_user_watch(
        session, user, filter.status, limit, offset
    )

    return {
        "pagination": pagination_dict(total, page, limit),
        "list": [watch for watch in result],
    }
