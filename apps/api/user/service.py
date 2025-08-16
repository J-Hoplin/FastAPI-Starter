import logging

from typing import Union
from apps.api.user.dto.request import ListUserFilter, CreateUser
from apps.api.user.exception import CredentialAlreadyExist
from apps.api.user.repository import UserRepository
from apps.core.auth.hash import hash_password
from apps.core.database.models import User
from sqlalchemy.exc import IntegrityError


logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def list_user(self, query_filter: ListUserFilter) -> Union[int, User]:
        return await self.user_repository.list_users(query_filter)

    async def retrieve_user(self, user_id: int) -> Union[User, None]:
        return await self.user_repository.retrieve_user_with_id(user_id)

    async def create_user(self, dto: CreateUser) -> User:
        try:
            return await self.user_repository.create_user(
                username=dto.username,
                email=dto.email,
                first_name=dto.first_name,
                last_name=dto.last_name,
                date_joined=dto.date_joined,
                hashed_password=hash_password(dto.password),
            )
        except IntegrityError:
            # Check unique constraint
            raise CredentialAlreadyExist()
