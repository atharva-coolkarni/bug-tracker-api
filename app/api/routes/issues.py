from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.schemas.issue import (
    IssueCreate,
    IssueUpdate,
    IssueResponse,
)
from app.api.deps.auth import get_current_user
from app.api.deps.permissions import require_roles
from app.db.deps import get_db
from app.models.issue import Issue
from app.models.project import Project
from app.models.user import User

router = APIRouter(
    prefix="/api/issues",
    tags=["issues"],
)

@router.post("", response_model=IssueResponse, status_code=201)
def create_issue(
    payload: IssueCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    project = db.get(Project, payload.project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    issue = Issue(
        title=payload.title,
        description=payload.description,
        priority=payload.priority,
        project_id=payload.project_id,
        created_by_id=current_user.id,
    )

    db.add(issue)
    db.commit()
    db.refresh(issue)

    return IssueResponse(
        id=str(issue.id),
        title=issue.title,
        description=issue.description,
        status=issue.status,
        priority=issue.priority,
        project_id=str(issue.project_id),
        created_by_id=str(issue.created_by_id),
        assignee_id=str(issue.assignee_id) if issue.assignee_id else None,
    )

@router.get("", response_model=list[IssueResponse])
def list_issues(
    project_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    issues = db.query(Issue).filter(Issue.project_id == project_id).all()

    return [
        IssueResponse(
            id=str(i.id),
            title=i.title,
            description=i.description,
            status=i.status,
            priority=i.priority,
            project_id=str(i.project_id),
            created_by_id=str(i.created_by_id),
            assignee_id=str(i.assignee_id) if i.assignee_id else None,
        )
        for i in issues
    ]

@router.put("/{issue_id}", response_model=IssueResponse)
def update_issue(
    issue_id: str,
    payload: IssueUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    issue = db.get(Issue, issue_id)
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")

    if (
        current_user.role not in ("admin", "manager")
        and issue.assignee_id != current_user.id
    ):
        raise HTTPException(status_code=403, detail="Not allowed")

    for field, value in payload.dict(exclude_unset=True).items():
        setattr(issue, field, value)

    db.commit()
    db.refresh(issue)

    return IssueResponse(
        id=str(issue.id),
        title=issue.title,
        description=issue.description,
        status=issue.status,
        priority=issue.priority,
        project_id=str(issue.project_id),
        created_by_id=str(issue.created_by_id),
        assignee_id=str(issue.assignee_id) if issue.assignee_id else None,
    )

@router.post(
    "/{issue_id}/assign/{user_id}",
    dependencies=[Depends(require_roles("admin", "manager"))],
)
def assign_issue(
    issue_id: str,
    user_id: str,
    db: Session = Depends(get_db),
):
    issue = db.get(Issue, issue_id)
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")

    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    issue.assignee_id = user.id
    db.commit()

    return {"detail": "Issue assigned"}

@router.post(
    "/{issue_id}/close",
    dependencies=[Depends(require_roles("admin", "manager"))],
)
def close_issue(
    issue_id: str,
    db: Session = Depends(get_db),
):
    issue = db.get(Issue, issue_id)
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")

    issue.status = "closed"
    db.commit()

    return {"detail": "Issue closed"}
