import uuid
from datetime import datetime, timedelta
from app.db.redis import redis_client
from app.schemas.session_schemas import Session

class SessionService:
    async def start_session(self, user_id: int, device_info: dict, duration_minutes: int) -> Session:
        session_id = str(uuid.uuid4())
        start_time = datetime.utcnow()
        remaining_time = duration_minutes * 60
        session_data = {
            "user_id": user_id,
            "device_info": str(device_info),
            "start_time": start_time.isoformat(),
            "remaining_time": remaining_time,
        }
        await redis_client.hmset(f"session:{session_id}", session_data)
        await redis_client.expire(f"session:{session_id}", remaining_time)
        return Session(id=session_id, device_info=device_info, start_time=start_time, remaining_time=remaining_time)

    async def get_active_sessions(self) -> list[Session]:
        sessions = []
        for key in await redis_client.keys("session:*"):
            session_data = await redis_client.hgetall(key)
            sessions.append(Session(
                id=key.split(":")[1],
                device_info=eval(session_data.get("device_info")),
                start_time=datetime.fromisoformat(session_data.get("start_time")),
                remaining_time=int(session_data.get("remaining_time"))
            ))
        return sessions

    async def end_session(self, session_id: str) -> Session:
        session_data = await redis_client.hgetall(f"session:{session_id}")
        if not session_data:
            return None
        await redis_client.delete(f"session:{session_id}")
        return Session(
            id=session_id,
            device_info=eval(session_data.get("device_info")),
            start_time=datetime.fromisoformat(session_data.get("start_time")),
            remaining_time=0
        )
