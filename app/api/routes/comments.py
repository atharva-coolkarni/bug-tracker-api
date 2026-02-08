from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.schemas.comment import CommentCreate, CommentResponse
from app.api.deps.auth import get_current_user
from app.db.deps import get_db
from app.models.comment import Comment
from app.models.issue import Issue
from app.models.user import User

router = APIRouter(
    prefix="/api/issues/{issue_id}/comments",
    tags=["comments"],
)

@router.post("", response_model=CommentResponse, status_code=201)
def add_comment(
    issue_id: str,
    payload: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    issue = db.get(Issue, issue_id)
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")

    comment = Comment(
        content=payload.content,
        issue_id=issue_id,
        user_id=current_user.id,
    )

    db.add(comment)
    db.commit()
    db.refresh(comment)

    return CommentResponse(
        id=str(comment.id),
        content=comment.content,
        issue_id=str(comment.issue_id),
        user_id=str(comment.user_id),
    )

@router.get("", response_model=list[CommentResponse])
def list_comments(
    issue_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    comments = db.query(Comment).filter(Comment.issue_id == issue_id).all()

    return [
        CommentResponse(
            id=str(c.id),
            content=c.content,
            issue_id=str(c.issue_id),
            user_id=str(c.user_id),
        )
        for c in comments
    ]

@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(
    issue_id: str,
    comment_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    comment = db.get(Comment, comment_id)
    if not comment or str(comment.issue_id) != issue_id:
        raise HTTPException(status_code=404, detail="Comment not found")

    if current_user.role != "admin" and comment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    db.delete(comment)
    db.commit()
