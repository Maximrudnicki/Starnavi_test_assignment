from fastapi import APIRouter, Depends, HTTPException

from schemas.user_shema import UserCreate, UserLogin, UserResponse, UserUpdate
from services.user_service import UserService
from repositories.user_repository import UserRepository
from models.user import User
from utils.auth import get_current_user
from .dependencies import get_user_service

router = APIRouter(
    prefix="/authentication",
    tags=["Authentication"],
)

user_service = UserService(UserRepository())


@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate, user_service: UserService = Depends(get_user_service)):
    user_id = user_service.create_user(user.username, user.email, user.password)
    return {"id": user_id, "username": user.username, "email": user.email}


@router.post("/login")
async def login(user: UserLogin, user_service: UserService = Depends(get_user_service)):
    return user_service.login(user.email, user.password)


@router.post("/update")
async def update(
    updates: UserUpdate,
    user_service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user),
):
    user_updates = updates.model_dump(exclude_unset=True)
    return user_service.update_user(current_user.id, user_updates)
