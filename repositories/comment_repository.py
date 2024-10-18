from datetime import datetime

from config.db import SessionLocal
from models.comment import Comment


class CommentRepository:
    def get_db(self):
        db = SessionLocal()
        try:
            return db
        finally:
            db.close()

    def create(self, comment: Comment) -> int:
        with self.get_db() as db:
            db.add(comment)
            db.commit()
            db.refresh(comment)
            return comment.id

    def get_by_id(self, comment_id: int) -> Comment | None:
        with self.get_db() as db:
            return db.query(Comment).filter(Comment.id == comment_id).first()

    def get_by_post(self, post_id: int) -> list[Comment]:
        with self.get_db() as db:
            return db.query(Comment).filter(Comment.post_id == post_id).all()

    def get_by_user(self, user_id: int) -> list[Comment]:
        with self.get_db() as db:
            return db.query(Comment).filter(Comment.user_id == user_id).all()

    def get_all(self) -> list[Comment]:
        with self.get_db() as db:
            return db.query(Comment).all()

    def update(self, comment_id: int, updates: dict) -> Comment | None:
        with self.get_db() as db:
            comment = db.query(Comment).filter(Comment.id == comment_id).first()
            if not comment:
                return None

            if 'is_banned' in updates:
                is_banned = updates['is_banned']
                if is_banned and not comment.is_banned:
                    updates['banned_at'] = datetime.now()
                elif not is_banned and comment.is_banned:
                    updates['banned_at'] = None

            for key, value in updates.items():
                if hasattr(comment, key):
                    setattr(comment, key, value)

            db.commit()
            db.refresh(comment)
            return comment

    def delete(self, comment_id: int) -> bool:
        with self.get_db() as db:
            comment = db.query(Comment).filter(Comment.id == comment_id).first()
            if not comment:
                return False
            db.delete(comment)
            db.commit()
            return True
