from fastapi import HTTPException, status

from repositories.post_repository import PostRepository
from models.post import Post


class PostService:
    def __init__(self, post_repository: PostRepository):
        self.post_repository = post_repository

    def create_post(self, title: str, text: str, author_id: int) -> int:
        post = Post(title=title, text=text, author_id=author_id)
        return self.post_repository.create(post)

    def get_post_by_id(self, post_id: int) -> Post | None:
        post = self.post_repository.get_by_id(post_id)
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Post not found."
            )
        return post

    def get_posts_by_author(self, author_id: int) -> list[Post]:
        return self.post_repository.get_by_author(author_id)

    def get_all_posts(self) -> list[Post]:
        return self.post_repository.get_all()

    def update_post(self, post_id: int, updates: dict) -> Post | None:
        post = self.post_repository.update(post_id, updates)
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Post not found."
            )
        return post

    def delete_post(self, post_id: int) -> bool:
        deleted = self.post_repository.delete(post_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Post not found."
            )
        return deleted
