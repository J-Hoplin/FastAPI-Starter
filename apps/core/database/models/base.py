from apps.core.database.db import Base
from datetime import datetime
from sqlalchemy import Column, DateTime


class RootModel(Base):
    """
    Base Model for application models

    Include: common fields, common methods

    """

    __abstract__ = True

    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(), nullable=False)
