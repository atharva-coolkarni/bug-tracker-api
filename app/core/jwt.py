from datetime import datetime, timedelta, timezone
from typing import Any

from jose import jwt

from app.core.config import settings


def _read_key(path: str) -> str:
    with open(path, "r") as f:
        return f.read()


PRIVATE_KEY = _read_key(settings.JWT_PRIVATE_KEY_PATH)
PUBLIC_KEY = _read_key(settings.JWT_PUBLIC_KEY_PATH)


def create_access_token(subject: str, role: str) -> str:
    expire = datetime.now(tz=timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    payload = {
        "sub": subject,
        "role": role,
        "exp": expire,
        "type": "access",
    }
    return jwt.encode(payload, PRIVATE_KEY, algorithm=settings.JWT_ALGORITHM)


def create_refresh_token(subject: str) -> str:
    expire = datetime.now(tz=timezone.utc) + timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )
    payload = {
        "sub": subject,
        "exp": expire,
        "type": "refresh",
    }
    return jwt.encode(payload, PRIVATE_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_token(token: str) -> dict[str, Any]:
    return jwt.decode(token, PUBLIC_KEY, algorithms=[settings.JWT_ALGORITHM])
