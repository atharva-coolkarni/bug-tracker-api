from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class Comment(BaseModel):
    __tablename__ = "comments"

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    issue_id: Mapped[str] = mapped_column(
        ForeignKey("issues.id", ondelete="CASCADE"),
        nullable=False,
    )

    author_id: Mapped[str] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
    )

    issue = relationship("Issue")
    author = relationship("User")
