import logging
from contextlib import asynccontextmanager, contextmanager
from asyncio import current_task

from typing import Generator, AsyncGenerator
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session, create_async_engine, async_sessionmaker


logger = logging.getLogger(__name__)

Base = declarative_base()

class Database:
    def __init__(self, database_url: str,debug: bool) -> None:
        self.database_url = database_url
        """
        pool_pre_ping: 미리 connection을 만들어 두고 생성된 connection미리 사용한다는 의미
        https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.pool_pre_ping
        
        expire_on_commit: SQLAlchemy Session이 Commit한 후에 ORM 속성들을 만료시킬지 여부
        """

        # Synchronous Engine and Session
        self.sync_engine = create_engine(
            database_url,
            pool_pre_ping=True,
            echo=debug,
        )
        self.sync_session_factory = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.sync_engine
        )

        # Asynchronous Engine and Session
        self.async_engine = create_async_engine(
            database_url,
            pool_pre_ping=True,
            echo=debug,
        )
        self.async_session_factory = async_scoped_session(
            async_sessionmaker(
                self.async_engine,
                expire_on_commit=False,
                autoflush=False,
            ),
            scopefunc=current_task
        )

    @asynccontextmanager
    async def async_session(self) -> AsyncGenerator[AsyncSession,None]:
        session: AsyncSession = self.async_session_factory()
        try:
            yield session
        except IntegrityError as exc:
            logger.error(f'Session rollback due to exception: {exc}')
            await session.rollback()
            raise
        except Exception as exc:
            logger.error(f'Session rollback due to exception: {exc}')
            if session.in_transaction():
                await session.rollback()
        finally:
            await session.close()
            await self.async_session_factory.remove()

    @contextmanager
    def sync_session(self) -> Generator[Session,None,None]:
        session: Session = self.sync_session_factory()
        try:
            yield session
        except IntegrityError as exception:
            logger.error('Sync session rollback because of exception: %s', exception)
            session.rollback()
        except Exception as exception:
            logger.error('Sync session rollback because of exception: %s', exception)
            if session.in_transaction():
                session.rollback()
        finally:
            session.close()

