from fastapi import HTTPException, status
from models.comment import Comment

from tasks.celery_tasks import auto_reply
from utils.filter import filter_text

from repositories.comment_repository import CommentRepository
from repositories.post_repository import PostRepository
from repositories.user_repository import UserRepository
from services.post_service import PostService
from services.user_service import UserService


class CommentService:
    def __init__(self, comment_repository: CommentRepository):
        self.comment_repository = comment_repository
        self.post_service = PostService(PostRepository())
        self.user_service = UserService(UserRepository())

    def create_comment(self, post_id: int, user_id: int, text: str) -> int:
        comment = Comment(post_id=post_id, user_id=user_id, text=text)
        comment_id = self.comment_repository.create(comment)

        try:
            self.check_comment_for_moderation(comment_id)
        except:
            return comment_id
        
        return comment_id

    def get_comment_by_id(self, comment_id: int) -> Comment | None:
        comment = self.comment_repository.get_by_id(comment_id)
        if not comment or comment.is_banned:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found."
            )
        return comment

    def get_comments_by_post(self, post_id: int) -> list[Comment]:
        comments = self.comment_repository.get_by_post(post_id)
        return [comment for comment in comments if not comment.is_banned]

    def get_comments_by_user(self, user_id: int) -> list[Comment]:
        comments = self.comment_repository.get_by_user(user_id)
        return [comment for comment in comments if not comment.is_banned]

    def get_all_comments(self) -> list[Comment]:
        comments = self.comment_repository.get_all()
        return [comment for comment in comments if not comment.is_banned]

    def update_comment(self, comment_id: int, updates: dict) -> Comment | None:
        comment = self.comment_repository.update(comment_id, updates)
        if not comment or comment.is_banned:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found."
            )
        return comment

    def delete_comment(self, comment_id: int) -> bool:
        deleted = self.comment_repository.delete(comment_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found."
            )
        return deleted

    def ban_comment(self, comment_id: int) -> Comment | None:
        updates = {"is_banned": True}
        comment = self.comment_repository.update(comment_id, updates)
        if not comment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found."
            )
        return comment
    
    def check_comment_for_moderation(self, comment_id: int):
        comment = self.get_comment_by_id(comment_id)
        if filter_text(comment.text):
            self.ban_comment(comment_id)
            return
        
        post = self.post_service.get_post_by_id(comment.post_id)
        author = self.user_service.get_by_id(post.author_id)
        if author.auto_reply_enabled:
            reply_text = f"`{comment.text}`, thank you for the comment!"
            auto_reply.apply_async((comment.post_id, reply_text), countdown=author.auto_reply_delay)
