from typing import Literal, Annotated

import jwt
from dependency_injector.wiring import Provide, inject
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from apps.api.user.repository import UserRepository
from apps.containers import Application
from apps.core.auth.exception import (
    TokenExpiredException,
    InvalidTokenException,
    InvalidCredentialException,
    RoleNotGrantedException,
)
from apps.core.database.models import User
from collections.abc import Iterable

"""
Parse JWT Token from authorization header.

See `__call__` magic method of OAuth2PasswordBearer class implementation
"""
bearer_scheme = HTTPBearer()


@inject
async def get_authenticated_user(
    token: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)],
    config: Annotated[dict, Depends(Provide[Application.config])],
    user_repository: Annotated[
        UserRepository, Depends(Provide[Application.user.repository])
    ],
) -> User:
    try:
        payload = jwt.decode(
            token.credentials,
            config.get("JWT_SECRET_KEY"),
            algorithms=[config.get("JWT_ALGORITHM")],
        )
        username: str | None = payload.get("sub")

        if username is None:
            raise InvalidCredentialException()

    except jwt.ExpiredSignatureError:
        raise TokenExpiredException()
    except jwt.InvalidTokenError:
        raise InvalidTokenException()

    user = await user_repository.retrieve_user_with_unique_clause(
        key="username", value=username, filter_is_active=True
    )

    if not user:
        raise InvalidCredentialException()
    return user


def role_granted_user(roles: Iterable[Literal["superuser", "staff"]]):
    for role in roles:
        assert role in ("superuser", "staff")

    async def allow_superuser_or_staff(
        user: Annotated[User, Depends(get_authenticated_user)]
    ):
        if not user.is_superuser or not user.is_staff:
            raise RoleNotGrantedException(expected_roles=roles)

        if user.is_superuser:
            return user

        if user.is_staff and "staff" not in roles:
            raise RoleNotGrantedException(expected_roles=roles)
        return user

    return allow_superuser_or_staff
