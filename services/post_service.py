from fastapi import HTTPException, status

from repositories.post_repository import PostRepository
from models.post import Post
from repositories.user_repository import UserRepository
from services.user_service import UserService
from tasks.celery_tasks import auto_reply
from utils.filter import filter_text


class PostService:
    def __init__(self, post_repository: PostRepository):
        self.post_repository = post_repository
        self.user_service = UserService(UserRepository())

    def create_post(self, title: str, text: str, author_id: int) -> int:
        post = Post(title=title, text=text, author_id=author_id)
        post_id = self.post_repository.create(post)

        self.check_post_for_moderation(post_id)

        return post_id

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
    
    def check_post_for_moderation(self, post_id: int):
        post = self.get_post_by_id(post_id)
        if filter_text(post.title) or filter_text(post.text):
            self.delete_post(post_id)
            return

        author = self.user_service.get_by_id(post.author_id)
        if author.auto_reply_enabled:
            reply_text = "Please, feel free to comment!"
            auto_reply.apply_async((post_id, reply_text), countdown=author.auto_reply_delay)
