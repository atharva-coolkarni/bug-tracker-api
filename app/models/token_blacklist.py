from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel


class TokenBlacklist(BaseModel):
    __tablename__ = "token_blacklist"

    jti: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        nullable=False,
        index=True,
    )

    token_type: Mapped[str] = mapped_column(
        String(10),
        nullable=False,  # access | refresh
    )
