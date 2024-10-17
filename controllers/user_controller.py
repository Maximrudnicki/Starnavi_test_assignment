from fastapi import APIRouter, Depends, HTTPException
from .dependencies import get_user_service
from schemas.user_shema import UserCreate, UserLogin, UserResponse
from services.user_service import UserService
from repositories.user_repository import UserRepository

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
