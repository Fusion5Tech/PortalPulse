from pydantic import BaseModel

class User(BaseModel):
    id: int
    username: str
    is_active: bool
    is_admin: bool

    class Config:
        orm_mode = True
