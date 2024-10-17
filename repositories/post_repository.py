from config.db import SessionLocal

from models.post import Post


class PostRepository:
    def get_db(self):
        db = SessionLocal()
        try:
            return db
        finally:
            db.close()

    def create(self, post: Post) -> int:
        with self.get_db() as db:
            db.add(post)
            db.commit()
            db.refresh(post)
            return post.id

    def get_by_id(self, post_id: int) -> Post | None:
        with self.get_db() as db:
            return db.query(Post).filter(Post.id == post_id).first()

    def get_by_author(self, author_id: int) -> list[Post]:
        with self.get_db() as db:
            return db.query(Post).filter(Post.author_id == author_id).all()

    def get_all(self) -> list[Post]:
        with self.get_db() as db:
            return db.query(Post).all()

    def update(self, post_id: int, updates: dict) -> Post | None:
        with self.get_db() as db:
            post = db.query(Post).filter(Post.id == post_id).first()
            if not post:
                return None
            for key, value in updates.items():
                if hasattr(post, key):
                    setattr(post, key, value)
            db.commit()
            db.refresh(post)
            return post

    def delete(self, post_id: int) -> bool:
        with self.get_db() as db:
            post = db.query(Post).filter(Post.id == post_id).first()
            if not post:
                return False
            db.delete(post)
            db.commit()
            return True

