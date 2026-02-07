from pydantic import BaseModel, Field
from typing import Optional


class IssueCreate(BaseModel):
    title: str = Field(..., max_length=200)
    description: Optional[str] = None
    priority: str = Field(..., examples=["low", "medium", "high"])
    project_id: str


class IssueUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None


class IssueResponse(BaseModel):
    id: str
    title: str
    description: Optional[str]
    status: str
    priority: str
    project_id: str
    created_by_id: str
    assignee_id: Optional[str]
