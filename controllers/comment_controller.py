from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from controllers.dependencies import get_comment_service
from models.user import User
from schemas.comment_schema import CommentCreate, CommentUpdate, CommentResponse
from services.comment_service import CommentService
from models.comment import Comment
from utils.auth import get_current_user

router = APIRouter(prefix="/comments", tags=["Comments"])


@router.post("/", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
def create_comment(
    comment: CommentCreate,
    current_user: User = Depends(get_current_user),
    comment_service: CommentService = Depends(get_comment_service),
):
    comment_id = comment_service.create_comment(
        post_id=comment.post_id, user_id=current_user.id, text=comment.text
    )
    return comment_service.get_comment_by_id(comment_id)


@router.get("/", response_model=List[CommentResponse])
def get_all_comments(comment_service: CommentService = Depends(get_comment_service)):
    return comment_service.get_all_comments()


@router.get("/{comment_id}", response_model=CommentResponse)
def get_comment(
    comment_id: int, comment_service: CommentService = Depends(get_comment_service)
):
    return comment_service.get_comment_by_id(comment_id)


@router.get("/post/{post_id}", response_model=List[CommentResponse])
def get_comments_by_post(
    post_id: int, comment_service: CommentService = Depends(get_comment_service)
):
    return comment_service.get_comments_by_post(post_id)


@router.get("/user/{user_id}", response_model=List[CommentResponse])
def get_comments_by_user(
    user_id: int, comment_service: CommentService = Depends(get_comment_service)
):
    return comment_service.get_comments_by_user(user_id)


@router.patch("/{comment_id}", response_model=CommentResponse)
def update_comment(
    comment_id: int,
    updates: CommentUpdate,
    comment_service: CommentService = Depends(get_comment_service),
):
    updated_comment = comment_service.update_comment(
        comment_id, updates.model_dump(exclude_unset=True)
    )
    return updated_comment


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(
    comment_id: int, comment_service: CommentService = Depends(get_comment_service)
):
    comment_service.delete_comment(comment_id)


@router.patch("/{comment_id}/ban", response_model=CommentResponse)
def ban_comment(
    comment_id: int, comment_service: CommentService = Depends(get_comment_service)
):
    return comment_service.ban_comment(comment_id)
