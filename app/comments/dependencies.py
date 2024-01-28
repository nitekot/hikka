from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import auth_required
from app.models import Comment, Edit, User
from datetime import datetime, timedelta
from app.database import get_session
from app.errors import Abort
from fastapi import Depends
from app import constants
from uuid import UUID
from . import service

from .schemas import (
    ContentTypeEnum,
    CommentArgs,
)


async def validate_content(
    slug: str,
    content_type: ContentTypeEnum,
    session: AsyncSession = Depends(get_session),
) -> Edit:
    if not (
        content := await service.get_content_by_slug(
            session, content_type, slug
        )
    ):
        raise Abort("comment", "content-not-found")

    return content


async def validate_content_slug(
    content: Edit = Depends(validate_content),
) -> str:
    return content.reference


async def validate_parent(
    args: CommentArgs,
    content_type: ContentTypeEnum,
    content_id: Edit = Depends(validate_content_slug),
    session: AsyncSession = Depends(get_session),
) -> Comment | None:
    if not args.parent:
        return None

    if not (
        parent_comment := await service.get_comment_by_content(
            session, content_type, content_id, args.parent
        )
    ):
        raise Abort("comment", "parent-not-found")

    max_reply_depth = 3
    if len(parent_comment.path) > max_reply_depth:
        raise Abort("comment", "max-depth")

    return parent_comment


async def validate_rate_limit(
    session: AsyncSession = Depends(get_session),
    author: User = Depends(
        auth_required(permissions=[constants.PERMISSION_COMMENT_WRITE])
    ),
):
    comments_limit = 100
    comments_total = await service.count_comments_limit(session, author)

    if comments_total >= comments_limit:
        raise Abort("comment", "rate-limit")

    return author


async def validate_comment(
    comment_reference: UUID,
    session: AsyncSession = Depends(get_session),
) -> Comment:
    if not (comment := await service.get_comment(session, comment_reference)):
        raise Abort("comment", "not-found")

    return comment


async def validate_comment_edit(
    comment: Comment = Depends(validate_comment),
    author: User = Depends(
        auth_required(permissions=[constants.PERMISSION_COMMENT_EDIT])
    ),
):
    time_limit = timedelta(hours=1)
    max_edits = 5

    if comment.author != author:
        raise Abort("comment", "not-owner")

    if len(comment.history) >= max_edits:
        raise Abort("comment", "max-edits")

    if datetime.utcnow() > comment.created + time_limit:
        raise Abort("comment", "edit-time-limit")

    return comment