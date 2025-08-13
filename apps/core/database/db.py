import logging
from contextlib import asynccontextmanager
from asyncio import current_task

from typing import AsyncGenerator
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    create_async_engine,
    async_sessionmaker,
)


logger = logging.getLogger(__name__)

Base = declarative_base()


class Database:
    def __init__(self, database_url: str, debug: bool) -> None:
        self.database_url = database_url
        """
        pool_pre_ping: 미리 connection을 만들어 두고 생성된 connection미리 사용한다는 의미
        https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine.params.pool_pre_ping

        expire_on_commit: SQLAlchemy Session이 Commit한 후에 ORM 속성들을 만료시킬지 여부
        """
        self.engine = create_async_engine(
            database_url,
            pool_pre_ping=True,
            echo=debug,
        )
        self.session_factory = async_scoped_session(
            async_sessionmaker(
                self.engine,
                expire_on_commit=False,
                autoflush=False,
            ),
            scopefunc=current_task,
        )

    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        session: AsyncSession = self.session_factory()
        try:
            yield session
        except IntegrityError as exc:
            logger.error(f"Session rollback due to integrity exception: {exc}")
            await session.rollback()
            raise
        except Exception as exc:
            logger.error(f"Session rollback due to exception: {exc}")
            if session.in_transaction():
                await session.rollback()
        finally:
            await session.close()
            await self.session_factory.remove()
