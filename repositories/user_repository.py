from config.db import SessionLocal

from models.user import User


class UserRepository:
    def get_db(self):
        db = SessionLocal()
        try:
            return db
        finally:
            db.close()

    def create(self, user: User) -> int:
        with self.get_db() as db:
            db.add(user)
            db.commit()
            db.refresh(user)
            return user.id
        
    def get_by_id(self, user_id: int) -> User | None:
        with self.get_db() as db:
            return db.query(User).filter(User.id == user_id).first()

    def get_all(self) -> list[User]:
        with self.get_db() as db:
            return db.query(User).all()

    def update(self, user_id: int, updates: dict) -> User | None:
        with self.get_db() as db:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                return None
            for key, value in updates.items():
                if hasattr(user, key):
                    setattr(user, key, value)
            db.commit()
            db.refresh(user)
            return user

    def delete(self, user_id: int) -> bool:
        with self.get_db() as db:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                return False
            db.delete(user)
            db.commit()
            return True
