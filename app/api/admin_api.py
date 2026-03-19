from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.session_schemas import Session as SessionSchema
from app.schemas.user_schemas import User as UserSchema
from app.schemas.voucher_schemas import (
    VoucherCreateRequest,
    VoucherOut,
    VoucherPrintItem,
    VoucherPrintResponse,
)
from app.services.admin_service import AdminService
from app.utils.dependencies import get_current_admin_user

router = APIRouter()
admin_service = AdminService()


@router.get("/users", response_model=list[UserSchema])
async def get_all_users(
    _current_user=Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):
    return await admin_service.get_all_users(db)


@router.get("/sessions", response_model=list[SessionSchema])
async def get_all_sessions(_current_user=Depends(get_current_admin_user)):
    return await admin_service.get_all_sessions()


@router.post("/sessions/{session_id}/disconnect", response_model=SessionSchema | None)
async def disconnect_user(
    session_id: str,
    _current_user=Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):
    return await admin_service.disconnect_user(session_id, db)


@router.get("/logs", response_model=list[dict])
async def get_logs(
    _current_user=Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):
    return await admin_service.get_logs(db)


@router.post("/vouchers", response_model=list[VoucherOut])
async def create_vouchers(
    payload: VoucherCreateRequest,
    _current_user=Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):
    return await admin_service.create_vouchers(payload, _current_user, db)


@router.get("/vouchers", response_model=list[VoucherOut])
async def list_vouchers(
    _current_user=Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):
    return await admin_service.list_vouchers(db)


@router.get("/vouchers/print", response_model=VoucherPrintResponse)
async def get_printable_vouchers(
    only_unprinted: bool = Query(True),
    _current_user=Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):
    vouchers = await admin_service.get_printable_vouchers(
        db, only_unprinted=only_unprinted
    )
    items = [
        VoucherPrintItem(code=v.code, duration_minutes=v.duration_minutes)
        for v in vouchers
    ]
    printable_text = "\n".join(
        f"Voucher: {item.code} | Duration: {item.duration_minutes} minutes"
        for item in items
    )
    return VoucherPrintResponse(vouchers=items, printable_text=printable_text)
