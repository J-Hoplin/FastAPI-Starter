from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from apps.api.user.repository import UserRepository
from apps.core.auth.hash import verify_password
from apps.core.database.db import Database


"""
SQLAdmin Authentication Backend

See document: https://aminalaee.github.io/sqladmin/api_reference/authentication/
"""


class AdminPageAuthentication(AuthenticationBackend):
    def __init__(self, secret_key: str, database: Database) -> None:
        super().__init__(secret_key)
        self.user_repository = UserRepository(database)

    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form.get("username"), form.get("password")

        if not username or not password:
            return False

        user = await self.user_repository.retrieve_superuser_or_staff(username=username)

        if not user:
            return False

        if not verify_password(password, user.hashed_password):
            return False

        if not (user.is_staff or user.is_superuser):
            return False

        request.session.update({"user_id": user.id, "username": user.username})
        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        user_id = request.session.get("user_id")
        if not user_id:
            return False

        user = await self.user_repository.retrieve_user_with_id(user_id)
        if not user or not user.is_active or not (user.is_staff or user.is_superuser):
            request.session.clear()
            return False

        return True
