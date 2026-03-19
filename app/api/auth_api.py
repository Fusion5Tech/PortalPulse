from fastapi import APIRouter
from app.services.auth_service import AuthService
from app.schemas.auth_schemas import LoginRequest, Token
from app.models.user_model import User
from app.utils.dependencies import get_current_user

router = APIRouter()
auth_service = AuthService()

@router.post("/login", response_model=Token)
async def login(login_request: LoginRequest):
    return await auth_service.login(login_request)

@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
