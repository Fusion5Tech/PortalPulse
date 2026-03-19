from fastapi import APIRouter, Depends

from app.services.session_service import SessionService
from app.schemas.session_schemas import Session
from app.utils.dependencies import get_current_user

router = APIRouter()
session_service = SessionService()


@router.get("/active", response_model=list[Session])
async def get_active_sessions(_current_user=Depends(get_current_user)):
    return await session_service.get_active_sessions()


@router.post("/{session_id}/end", response_model=Session)
async def end_session(session_id: str, _current_user=Depends(get_current_user)):
    return await session_service.end_session(session_id)
