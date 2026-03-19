from pydantic import BaseModel
import datetime

class Session(BaseModel):
    id: str
    device_info: dict
    start_time: datetime.datetime
    remaining_time: int
