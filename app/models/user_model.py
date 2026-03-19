from sqlalchemy import Column, Integer, String, Boolean, DateTime
from app.db.session import Base
import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)

class SessionLog(Base):
    __tablename__ = "session_logs"

    id = Column(Integer, primary_key=True, index=True)
    ip_address = Column(String)
    mac_address = Column(String)
    login_time = Column(DateTime, default=datetime.datetime.utcnow)
    logout_time = Column(DateTime)
    user_id = Column(Integer)
