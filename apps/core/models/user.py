from apps.core.database.db import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum,Text
from datetime import datetime
import enum


class UserRole(enum.Enum):
    USER = "user"
    STAFF = "staff"
    SUPERUSER = "superuser"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(20), index=True, unique=True, nullable=False)
    email = Column(String(150), index=True, unique=True, nullable=False)
    first_name = Column(String(10), nullable=True)
    last_name = Column(String(10), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    is_staff = Column(Boolean, default=False, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.USER, nullable=False)
    date_joined = Column(DateTime, default=datetime.now(), nullable=False)
    last_login = Column(DateTime, nullable=True)
    hashed_password = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(), nullable=False)
