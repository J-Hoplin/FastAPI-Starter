from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from apps.core.config import settings
from loguru import logger

engine = create_engine(settings.DATABASE_URL, echo=settings.DEBUG)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def create_db_and_tables():
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database Model Initialized")
    except Exception as e:
        logger.error(f"Exception: {e}")
        raise


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()