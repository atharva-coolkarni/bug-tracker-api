from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.issue import Issue
from app.models.user import User
from app.api.deps.auth import get_current_user


def require_issue_owner_or_admin(
    issue_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    issue = db.get(Issue, issue_id)
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")

    if (
        current_user.role != "admin"
        and issue.assignee_id != current_user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to modify this issue",
        )

    return issue
