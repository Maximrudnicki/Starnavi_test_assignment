from models.user import User
from repositories.user_repository import UserRepository
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext
from fastapi import HTTPException, status
from utils.auth import create_access_token


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def create_user(self, username: str, email: str, password: str) -> int:
        hashed_password = self.pwd_context.hash(password)
        user = User(username=username, email=email, password=hashed_password)
        try:
            return self.user_repository.create(user)
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered."
            )

    def login(self, email: str, password: str):
        user = self.user_repository.get_by_email(email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found."
            )
        
        if user.is_banned:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User is banned."
            )

        if not self.pwd_context.verify(password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid password."
            )
        
        access_token = create_access_token(data={"sub": email, "id": user.id})
        return {"access_token": access_token, "token_type": "bearer"}

    def get_by_id(self, user_id: int) -> User | None:
        return self.user_repository.get_by_id(user_id)

    def update_user(self, user_id: int, updates: dict) -> User | None:
        return self.user_repository.update(user_id, updates)

    def delete_user(self, user_id: int) -> bool:
        return self.user_repository.delete(user_id)

    def ban_user(self, user_id: int) -> User | None:
        updates = {"is_banned": True}
        return self.user_repository.update(user_id, updates)
