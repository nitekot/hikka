from .service import get_edit_by_id, get_content_by_id, get_content_by_slug
from .schemas import ContentTypeEnum, AnimeEditArgs
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import auth_required
from app.database import get_session
from app.errors import Abort
from fastapi import Depends
from app import constants
from typing import Union


from app.models import (
    AnimeStaffRole,
    ContentEdit,
    AnimeGenre,
    Character,
    Company,
    Person,
    Anime,
    User,
)


async def validate_edit_perms(
    session: AsyncSession = Depends(get_session),
    user: User = Depends(
        auth_required(permissions=[constants.PERMISSION_CREATE_EDIT])
    ),
) -> User:
    return user


async def validate_review_perms(
    session: AsyncSession = Depends(get_session),
    user: User = Depends(
        auth_required(
            permissions=[
                constants.PERMISSION_ACCEPT_EDIT,
                constants.PERMISSION_REJECT_EDIT,
            ]
        )
    ),
) -> User:
    return user


async def validate_edit_id(
    edit_id: int,
    session: AsyncSession = Depends(get_session),
) -> ContentEdit:
    if not (edit := await get_edit_by_id(session, edit_id)):
        raise Abort("edit", "invalid-id")

    return edit


async def validate_edit_content_type(
    content_type: ContentTypeEnum,
    edit: ContentEdit = Depends(validate_edit_id),
    session: AsyncSession = Depends(get_session),
) -> ContentEdit:
    if edit.status != constants.EDIT_PENDING:
        raise Abort("edit", "already-reviewed")

    if edit.content_type != content_type:
        raise Abort("edit", "wrong-content-type")

    if not (await get_content_by_id(session, content_type, edit.content_id)):
        raise Abort("edit", "invalid-content-id")

    return edit


# Here we make sure that there aren't any invalid keys and that the edits
# are actually different compared to the current version
async def validate_edit_approval(
    content_type: ContentTypeEnum,
    edit: ContentEdit = Depends(validate_edit_content_type),
    session: AsyncSession = Depends(get_session),
) -> ContentEdit:
    content = await get_content_by_id(session, content_type, edit.content_id)

    pop_list = []

    for key, value in edit.after.items():
        if not hasattr(content, key):
            raise Abort("edit", "invalid-field")

        if getattr(content, key) == value:
            pop_list.append(key)

    for pop_key in pop_list:
        edit.after.pop(pop_key)

    if len(edit.after) <= 0:
        raise Abort("edit", "empty-edit")

    return edit


async def validate_content_slug(
    slug: str,
    content_type: ContentTypeEnum,
    session: AsyncSession = Depends(get_session),
) -> Union[Anime, Character, Company, AnimeGenre, Person, AnimeStaffRole, None]:
    if not (content := await get_content_by_slug(session, content_type, slug)):
        raise Abort("edit", "content-not-found")

    return content


# ToDo: move this to a model_validator once we migrate to Pydantic 2
async def validate_args(args: AnimeEditArgs) -> AnimeEditArgs:
    for arg in args:
        if arg[1] is not None:
            return args

    raise Abort("edit", "empty-edit")