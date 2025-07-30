from fastapi import APIRouter
from controllers.auth_controller import register_user, login_user
from models.user import UserCreate, UserLogin

router = APIRouter(tags=["Authentication"])

@router.post("/register", summary="Register new user")
async def register(user: UserCreate):
    return await register_user(user)

@router.post("/login", summary="User login")
async def login(credentials: UserLogin):
    return await login_user(credentials)