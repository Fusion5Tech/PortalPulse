from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user_model import User, SessionLog
from app.services.session_service import SessionService

class AdminService:
    def __init__(self):
        self.session_service = SessionService()

    async def get_all_users(self, db: Session = next(get_db())) -> list[User]:
        return db.query(User).all()

    async def get_all_sessions(self):
        return await self.session_service.get_active_sessions()

    async def disconnect_user(self, session_id: str):
        return await self.session_service.end_session(session_id)

    async def get_logs(self, db: Session = next(get_db())) -> list[dict]:
        logs = db.query(SessionLog).all()
        return [
            {
                "ip_address": log.ip_address,
                "mac_address": log.mac_address,
                "login_time": log.login_time,
                "logout_time": log.logout_time,
                "user_id": log.user_id,
            }
            for log in logs
        ]
