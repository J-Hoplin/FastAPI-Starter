from sqlalchemy import select, func, or_, and_
from datetime import datetime
from typing import Literal, Tuple, List

from apps.api.user.schemas.request import ListUserFilter
from apps.core.database.db import Database
from apps.core.database.models import User


class UserRepository:
    def __init__(self, database: Database):
        self.db = database

    async def list_users(self, query_filter: ListUserFilter):
        offset = query_filter.get_offset()
        conditions = []

        if query_filter.name:
            conditions.append(User.first_name.ilike(f"%{query_filter.username}%"))
            conditions.append(User.last_name.ilike(f"%{query_filter.username}%"))

        if query_filter.email:
            conditions.append(User.email.ilike(f"%{query_filter.email}%"))

        if query_filter.is_active:
            conditions.append(User.is_active.is_(True))

        async with self.db.session() as session:
            query = (
                select(User)
                .order_by(User.id)
                .where(*conditions)
                .offset(offset)
                .limit(query_filter.limit)
            )
            users = (await session.execute(query)).scalars().all()

            if conditions:
                total = await session.scalar(
                    select(func.count()).select_from(
                        select(User.id).where(*conditions).subquery()
                    )
                )
            else:
                total = await session.scalar(select(func.count()).select_from(User))

            return total, users

    async def retrieve_user_with_id(self, user_id: int):
        async with self.db.session() as session:
            query = select(User).where(User.id == user_id)
            user = (await session.execute(query)).scalar()
            if user:
                return user
            else:
                return None

    async def retrieve_user_with_unique_clause(
        self,
        key: Literal["username", "email"],
        value: str,
        filter_is_active: bool = False,
    ) -> User:
        assert key in ("username", "email")
        assert value is not None

        where_clause = []
        if key == "username":
            where_clause.append(User.username == value)
        elif key == "email":
            where_clause.append(User.email == value)

        if filter_is_active:
            where_clause.append(User.is_active.is_(True))

        async with self.db.session() as session:
            query = select(User).where(*where_clause)
            user = (await session.execute(query)).scalar()
            if user:
                return user
            else:
                return None

    async def check_user_exists(self, username: str = None, email: str = None):
        async with self.db.session() as session:
            conflicts = []

            if username:
                existing_username = await session.scalar(
                    select(User).where(User.username == username)
                )
                if existing_username:
                    conflicts.append("username")

            if email:
                existing_email = await session.scalar(
                    select(User).where(User.email == email)
                )
                if existing_email:
                    conflicts.append("email")

            return conflicts

    async def retrieve_superuser_or_staff(self, username: str):
        async with self.db.session() as session:
            query = select(User).where(
                and_(
                    User.username == username,
                    User.is_active.is_(True),
                    or_(User.is_superuser.is_(True), User.is_staff.is_(True)),
                )
            )

            user = (await session.execute(query)).scalar()
            if user:
                return user
            else:
                return None

    async def create_user(
        self,
        username: str,
        email: str,
        first_name: str,
        last_name: str,
        date_joined: datetime,
        hashed_password: str,
    ) -> Tuple[User | None, List[str] | None]:
        """
        Returns

        - Val 1: Created user
        - Val 2: Conflicted unique clauses
        """

        conflicts = await self.check_user_exists(username=username, email=email)

        if conflicts:
            return None, conflicts

        async with self.db.session() as session:
            new_user = User(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                date_joined=date_joined,
                hashed_password=hashed_password,
            )

            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)

            return new_user, None
