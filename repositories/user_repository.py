from config.db import SessionLocal

from models.user import User


class UserRepository:
    def get_db(self):
        db = SessionLocal()
        try:
            return db
        finally:
            db.close()
