from apps.core.database.models.base import RootModel
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, Text
from datetime import datetime
import enum


class UserProviderType(enum.Enum):
    LOCAL = "local"
    GOOGLE = "google"
    APPLE = "apple"


class User(RootModel):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(20), index=True, unique=True, nullable=False)
    email = Column(String(150), index=True, unique=True, nullable=False)
    first_name = Column(String(10), nullable=True)
    last_name = Column(String(10), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    is_staff = Column(Boolean, default=False, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    date_joined = Column(DateTime, default=datetime.now(), nullable=False)
    last_login = Column(DateTime, nullable=True)
    hashed_password = Column(Text, nullable=False)
    provider_type = Column(
        Enum(UserProviderType), default=UserProviderType.LOCAL, nullable=False
    )
    provider_id = Column(String(150), nullable=True)
