from pydantic import BaseModel
from typing import Optional


class CommentCreate(BaseModel):
    content: str


class CommentResponse(BaseModel):
    id: str
    content: str
    issue_id: str
    user_id: str
