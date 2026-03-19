from fastapi import APIRouter, Depends
from app.services.admin_service import AdminService
from app.schemas.user_schemas import User
from app.schemas.session_schemas import Session
from app.utils.dependencies import get_current_admin_user

router = APIRouter()
admin_service = AdminService()

@router.get("/admin/users", response_model=list[User])
async def get_all_users(current_user: User = Depends(get_current_admin_user)):
    return await admin_service.get_all_users()

@router.get("/admin/sessions", response_model=list[Session])
async def get_all_sessions(current_user: User = Depends(get_current_admin_user)):
    return await admin_service.get_all_sessions()

@router.post("/admin/sessions/{session_id}/disconnect", response_model=Session)
async def disconnect_user(session_id: str, current_user: User = Depends(get_current_admin_user)):
    return await admin_service.disconnect_user(session_id)

@router.get("/admin/logs", response_model=list[dict])
async def get_logs(current_user: User = Depends(get_current_admin_user)):
    return await admin_service.get_logs()
