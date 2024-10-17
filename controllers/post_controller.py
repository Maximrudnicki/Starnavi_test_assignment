from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from services.post_service import PostService
from schemas.post_schema import PostCreate, PostUpdate, PostResponse
from utils.auth import get_current_user
from models.user import User
from .dependencies import get_post_service

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.post("/", response_model=PostResponse)
def create_post(
    post_data: PostCreate,
    current_user: User = Depends(get_current_user),
    post_service: PostService = Depends(get_post_service),
):
    post_id = post_service.create_post(
        title=post_data.title, text=post_data.text, author_id=current_user.id
    )
    return post_service.get_post_by_id(post_id)


@router.get("/{post_id}", response_model=PostResponse)
def get_post_by_id(post_id: int, post_service: PostService = Depends(get_post_service)):
    return post_service.get_post_by_id(post_id)


@router.get("/author/{author_id}", response_model=List[PostResponse])
def get_posts_by_author(
    author_id: int, post_service: PostService = Depends(get_post_service)
):
    return post_service.get_posts_by_author(author_id)


@router.get("/", response_model=List[PostResponse])
def get_all_posts(post_service: PostService = Depends(get_post_service)):
    return post_service.get_all_posts()


@router.patch("/{post_id}", response_model=PostResponse)
def update_post(
    post_id: int,
    post_data: PostUpdate,
    current_user: User = Depends(get_current_user),
    post_service: PostService = Depends(get_post_service),
):
    post = post_service.get_post_by_id(post_id)

    if post.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to update this post.",
        )

    return post_service.update_post(post_id, post_data.model_dump(exclude_unset=True))


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    post_service: PostService = Depends(get_post_service),
):
    post = post_service.get_post_by_id(post_id)

    if post.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to delete this post.",
        )

    post_service.delete_post(post_id)
    return None
