from pydantic import BaseModel
import datetime


class Session(BaseModel):
    id: str
    device_info: dict
    start_time: datetime.datetime
    remaining_time: int
    auth_method: str | None = None
    user_id: int | None = None
    voucher_code: str | None = None
