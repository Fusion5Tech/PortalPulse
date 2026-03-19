import json
import uuid
from datetime import datetime

from app.db.redis import redis_client
from app.schemas.session_schemas import Session


class SessionService:
    async def start_session(
        self,
        duration_minutes: int,
        device_info: dict,
        auth_method: str,
        user_id: int | None = None,
        voucher_code: str | None = None,
    ) -> Session:
        session_id = str(uuid.uuid4())
        start_time = datetime.utcnow()
        remaining_time = duration_minutes * 60
        session_data = {
            "user_id": "" if user_id is None else str(user_id),
            "voucher_code": voucher_code or "",
            "auth_method": auth_method,
            "device_info": json.dumps(device_info),
            "start_time": start_time.isoformat(),
        }
        await redis_client.hset(f"session:{session_id}", mapping=session_data)
        await redis_client.expire(f"session:{session_id}", remaining_time)
        return Session(
            id=session_id,
            device_info=device_info,
            start_time=start_time,
            remaining_time=remaining_time,
            auth_method=auth_method,
            user_id=user_id,
            voucher_code=voucher_code,
        )

    async def get_active_sessions(self) -> list[Session]:
        sessions = []
        for key in await redis_client.keys("session:*"):
            session_data = await redis_client.hgetall(key)
            ttl = await redis_client.ttl(key)
            remaining = max(ttl, 0)
            user_id_raw = session_data.get("user_id") or ""
            sessions.append(
                Session(
                    id=key.split(":")[1],
                    device_info=json.loads(session_data.get("device_info") or "{}"),
                    start_time=datetime.fromisoformat(session_data.get("start_time")),
                    remaining_time=remaining,
                    auth_method=session_data.get("auth_method"),
                    user_id=int(user_id_raw) if user_id_raw else None,
                    voucher_code=session_data.get("voucher_code") or None,
                )
            )
        return sessions

    async def end_session(self, session_id: str) -> Session | None:
        session_data = await redis_client.hgetall(f"session:{session_id}")
        if not session_data:
            return None
        await redis_client.delete(f"session:{session_id}")
        user_id_raw = session_data.get("user_id") or ""
        return Session(
            id=session_id,
            device_info=json.loads(session_data.get("device_info") or "{}"),
            start_time=datetime.fromisoformat(session_data.get("start_time")),
            remaining_time=0,
            auth_method=session_data.get("auth_method"),
            user_id=int(user_id_raw) if user_id_raw else None,
            voucher_code=session_data.get("voucher_code") or None,
        )
