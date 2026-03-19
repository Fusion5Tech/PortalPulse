from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String

from app.db.session import Base


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
    device_name = Column(String, nullable=True)
    auth_method = Column(String, nullable=False, default="voucher")
    voucher_code = Column(String, nullable=True)
    session_id = Column(String, nullable=True)
    login_time = Column(DateTime, default=datetime.utcnow)
    logout_time = Column(DateTime)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)


class Voucher(Base):
    __tablename__ = "vouchers"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True, nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True)
    is_used = Column(Boolean, default=False)
    printed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    expires_at = Column(DateTime, nullable=True)
    used_at = Column(DateTime, nullable=True)
    created_by_admin_id = Column(Integer, ForeignKey("users.id"), nullable=False)
