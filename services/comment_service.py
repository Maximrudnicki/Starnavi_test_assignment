from fastapi import HTTPException, status
from repositories.comment_repository import CommentRepository
from models.comment import Comment


class CommentService:
    def __init__(self, comment_repository: CommentRepository):
        self.comment_repository = comment_repository

    def create_comment(self, post_id: int, user_id: int, text: str) -> int:
        comment = Comment(post_id=post_id, user_id=user_id, text=text)
        return self.comment_repository.create(comment)

    def get_comment_by_id(self, comment_id: int) -> Comment | None:
        comment = self.comment_repository.get_by_id(comment_id)
        if not comment or comment.is_banned :
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found."
            )
        print(comment)
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
