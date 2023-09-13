# Todo: replace validator with field_validator once we migrate to Pydantic 2
from pydantic import Field, HttpUrl, validator
from datetime import datetime
from app import constants
from typing import Union
from enum import Enum
from uuid import UUID

from app.schemas import (
    PaginationResponse,
    ORJSONModel,
)


class EditArgs(ORJSONModel):
    description: Union[str, None] = Field(example="...")


class AnimeExternal(ORJSONModel):
    url: HttpUrl = Field(example="https://demonslayer-anime.com/mugentrainarc/")
    text: str = Field(example="Official Site", max_length=255)


class AnimeVideoTypeEnum(str, Enum):
    video_promo = constants.VIDEO_PROMO
    video_music = constants.VIDEO_MUSIC


class AnimeVideo(ORJSONModel):
    url: HttpUrl = Field(example="https://youtu.be/_4W1OQoDEDg")
    title: Union[str, None] = Field(
        example="ED 2 (Artist ver.)", max_length=255
    )
    description: Union[str, None] = Field(example="...")
    video_type: AnimeVideoTypeEnum = Field(example="video_music")


class AnimeOSTTypeEnum(str, Enum):
    opening = constants.OST_OPENING
    ending = constants.OST_ENDING


class AnimeOST(ORJSONModel):
    # ToDo: Some more sanity checks like making sure that the indexes are in
    # the correct order
    index: int = Field(example=1)
    title: Union[str, None] = Field(example="fantastic dreamer", max_length=255)
    author: Union[str, None] = Field(example="Machico", max_length=255)
    spotify: Union[HttpUrl, None] = Field(
        example="https://open.spotify.com/track/3BIhcWQV2hGRoEXdLL3Fzw"
    )
    ost_type: AnimeOSTTypeEnum = Field(example="opening")


class AnimeEditArgs(EditArgs):
    title_ja: Union[str, None] = Field(
        example="Kimetsu no Yaiba: Mugen Ressha-hen", max_length=255
    )
    title_en: Union[str, None] = Field(
        example="Demon Slayer: Kimetsu no Yaiba Mugen Train Arc", max_length=255
    )
    title_ua: Union[str, None] = Field(
        example="Клинок, який знищує демонів: Арка Нескінченного потяга",
        max_length=255,
    )
    synopsis_en: Union[str, None] = Field(example="...")
    synopsis_ua: Union[str, None] = Field(example="...")

    synonyms: Union[list[str], None] = Field()
    # external: Union[list[AnimeExternal], None] = Field()
    # videos: Union[list[AnimeVideo], None] = Field()
    # ost: Union[list[AnimeOST], None] = Field()

    # poster: Union[HttpUrl, None] = Field()


class EditStatusEnum(str, Enum):
    edit_pending = constants.EDIT_PENDING
    edit_approved = constants.EDIT_APPROVED
    edit_denied = constants.EDIT_DENIED
    edit_closed = constants.EDIT_CLOSED


class ContentTypeEnum(str, Enum):
    content_anime = constants.CONTENT_ANIME
    content_manga = constants.CONTENT_MANGA
    content_character = constants.CONTENT_CHARACTER
    content_company = constants.CONTENT_COMPANY
    content_episode = constants.CONTENT_EPISODE
    content_genre = constants.CONTENT_GENRE
    content_person = constants.CONTENT_PERSON
    content_staff = constants.CONTENT_STAFF


class UserResponse(ORJSONModel):
    username: str = Field(example="hikka")


class EditResponse(ORJSONModel):
    edit_id: int = Field(example=3)
    status: EditStatusEnum = Field(example="pending")
    created: datetime = Field(example=1693850684)
    updated: datetime = Field(example=1693850684)

    description: Union[str, None] = Field(example="...")
    hidden: bool = Field(example=False)

    content_id: UUID = Field(example="2a407b0c-e28c-4bc4-80bb-d54f8e4c51a6")
    content_type: ContentTypeEnum = Field(example="anime")

    before: Union[dict, None] = Field()
    after: dict = Field()

    # Note that this will generate a wrong return type in the docs
    # Should be fixed after migrating to Pydantic 2
    author: UserResponse = Field()
    moderator: Union[UserResponse, None] = Field()

    @validator("author")
    def convert_author(cls, author: UserResponse) -> str:
        return author.username

    @validator("moderator")
    def convert_moderator(
        cls, moderator: Union[UserResponse, None]
    ) -> Union[str, None]:
        return moderator.username if moderator else None


class EditListResponse(ORJSONModel):
    pagination: PaginationResponse
    list: list[EditResponse]