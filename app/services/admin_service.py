import secrets
import string
from datetime import datetime

from sqlalchemy.orm import Session

from app.models.user_model import SessionLog, User, Voucher
from app.schemas.voucher_schemas import VoucherCreateRequest
from app.services.session_service import SessionService


class AdminService:
    def __init__(self) -> None:
        self.session_service = SessionService()

    async def get_all_users(self, db: Session) -> list[User]:
        return db.query(User).all()

    async def get_all_sessions(self):
        return await self.session_service.get_active_sessions()

    async def disconnect_user(self, session_id: str, db: Session):
        ended = await self.session_service.end_session(session_id)
        if ended:
            log = (
                db.query(SessionLog)
                .filter(
                    SessionLog.session_id == session_id,
                    SessionLog.logout_time.is_(None),
                )
                .order_by(SessionLog.login_time.desc())
                .first()
            )
            if log:
                log.logout_time = datetime.utcnow()
                db.commit()
        return ended

    async def get_logs(self, db: Session) -> list[dict]:
        logs = db.query(SessionLog).order_by(SessionLog.login_time.desc()).all()
        return [
            {
                "ip_address": log.ip_address,
                "mac_address": log.mac_address,
                "device_name": log.device_name,
                "auth_method": log.auth_method,
                "voucher_code": log.voucher_code,
                "session_id": log.session_id,
                "login_time": log.login_time,
                "logout_time": log.logout_time,
                "user_id": log.user_id,
            }
            for log in logs
        ]

    async def create_vouchers(
        self,
        payload: VoucherCreateRequest,
        admin_user: User,
        db: Session,
    ) -> list[Voucher]:
        created: list[Voucher] = []
        for _ in range(payload.count):
            code = self._generate_unique_voucher_code(db)
            voucher = Voucher(
                code=code,
                duration_minutes=payload.duration_minutes,
                created_by_admin_id=admin_user.id,
            )
            db.add(voucher)
            created.append(voucher)
        db.commit()

        for voucher in created:
            db.refresh(voucher)
        return created

    async def list_vouchers(self, db: Session) -> list[Voucher]:
        return db.query(Voucher).order_by(Voucher.created_at.desc()).all()

    async def get_printable_vouchers(
        self, db: Session, only_unprinted: bool = True
    ) -> list[Voucher]:
        query = db.query(Voucher).filter(
            Voucher.is_active.is_(True), Voucher.is_used.is_(False)
        )
        if only_unprinted:
            query = query.filter(Voucher.printed.is_(False))

        vouchers = query.order_by(Voucher.created_at.asc()).all()
        for voucher in vouchers:
            voucher.printed = True
        db.commit()
        return vouchers

    def _generate_unique_voucher_code(self, db: Session, length: int = 10) -> str:
        alphabet = string.ascii_uppercase + string.digits
        while True:
            code = "".join(secrets.choice(alphabet) for _ in range(length))
            exists = db.query(Voucher).filter(Voucher.code == code).first()
            if not exists:
                return code
