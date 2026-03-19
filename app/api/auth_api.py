from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.auth_service import AuthService
from app.schemas.auth_schemas import LoginRequest, Token
from app.schemas.user_schemas import User as UserSchema
from app.utils.dependencies import get_current_admin_user

router = APIRouter()
auth_service = AuthService()


@router.post("/login", response_model=Token)
async def login(login_request: LoginRequest, db: Session = Depends(get_db)):
    return await auth_service.login(login_request, db)


@router.get("/me", response_model=UserSchema)
async def read_users_me(current_user=Depends(get_current_admin_user)):
    return current_user
