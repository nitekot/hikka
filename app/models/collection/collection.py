from sqlalchemy.dialects.postgresql import ARRAY
from ..mixins import CreatedMixin, UpdatedMixin
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy import ForeignKey
from sqlalchemy import String
from ..base import Base


class Collection(Base, CreatedMixin, UpdatedMixin):
    __tablename__ = "service_collections"

    # ToDo: moderated

    labels_order: Mapped[list[str]] = mapped_column(ARRAY(String))
    description: Mapped[str] = mapped_column(nullable=True)
    tags: Mapped[list[str]] = mapped_column(ARRAY(String))
    content_type: Mapped[str] = mapped_column(index=True)
    spoiler: Mapped[bool] = mapped_column(default=False)
    nsfw: Mapped[bool] = mapped_column(default=False)
    title: Mapped[str] = mapped_column(String(255))
    private: Mapped[bool]
    entries: Mapped[int]

    author_id = mapped_column(ForeignKey("service_users.id"))
    author: Mapped["User"] = relationship(
        foreign_keys=[author_id],
        lazy="selectin",
    )
