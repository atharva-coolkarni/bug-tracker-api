from pydantic import BaseModel, Field


class ProjectCreate(BaseModel):
    name: str = Field(..., max_length=100)
    description: str | None = None


class ProjectUpdate(BaseModel):
    name: str | None = Field(None, max_length=100)
    description: str | None = None


class ProjectResponse(BaseModel):
    id: str
    name: str
    description: str | None
