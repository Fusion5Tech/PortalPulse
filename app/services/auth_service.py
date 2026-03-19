from datetime import datetime, timedelta

from fastapi import HTTPException
from jose import jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import verify_password
from app.models.user_model import SessionLog, User, Voucher
from app.schemas.auth_schemas import LoginRequest
from app.services.session_service import SessionService


class AuthService:
    def __init__(self) -> None:
        self.session_service = SessionService()

    def create_access_token(
        self, data: dict, expires_delta: timedelta | None = None
    ) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + (
            expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    async def login(self, login_request: LoginRequest, db: Session) -> dict:
        if login_request.voucher_code:
            return await self._login_with_voucher(login_request, db)
        return await self._login_admin(login_request, db)

    async def _login_admin(self, login_request: LoginRequest, db: Session) -> dict:
        user = db.query(User).filter(User.username == login_request.username).first()
        if not user or not verify_password(
            login_request.password or "", user.hashed_password
        ):
            raise HTTPException(status_code=401, detail="Invalid admin credentials")
        if not user.is_admin:
            raise HTTPException(
                status_code=403,
                detail="Username/password login is restricted to admins",
            )

        access_token = self.create_access_token(
            data={"sub": user.username, "role": "admin", "user_id": user.id}
        )
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "role": "admin",
            "session_id": None,
        }

    async def _login_with_voucher(
        self, login_request: LoginRequest, db: Session
    ) -> dict:
        voucher = (
            db.query(Voucher).filter(Voucher.code == login_request.voucher_code).first()
        )
        if not voucher:
            raise HTTPException(status_code=401, detail="Invalid voucher")
        if not voucher.is_active:
            raise HTTPException(status_code=403, detail="Voucher is inactive")
        if voucher.is_used:
            raise HTTPException(status_code=403, detail="Voucher already used")
        if voucher.expires_at and voucher.expires_at <= datetime.utcnow():
            raise HTTPException(status_code=403, detail="Voucher expired")

        device_info = {
            "ip_address": login_request.ip_address,
            "mac_address": login_request.mac_address,
            "device_name": login_request.device_name,
        }
        session = await self.session_service.start_session(
            duration_minutes=voucher.duration_minutes,
            device_info=device_info,
            auth_method="voucher",
            voucher_code=voucher.code,
        )

        voucher.is_used = True
        voucher.used_at = datetime.utcnow()

        db.add(
            SessionLog(
                ip_address=login_request.ip_address,
                mac_address=login_request.mac_address,
                device_name=login_request.device_name,
                auth_method="voucher",
                voucher_code=voucher.code,
                session_id=session.id,
                user_id=None,
            )
        )
        db.commit()

        access_token = self.create_access_token(
            data={
                "sub": f"voucher:{voucher.code}",
                "role": "voucher",
                "voucher_code": voucher.code,
                "session_id": session.id,
            },
            expires_delta=timedelta(minutes=voucher.duration_minutes),
        )
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "role": "voucher",
            "session_id": session.id,
        }
