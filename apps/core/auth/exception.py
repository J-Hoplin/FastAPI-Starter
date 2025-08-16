from collections.abc import Iterable
from apps.core.exception.base import RootException
from fastapi import status


class TokenExpiredException(RootException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, message="Token Expired"
        )


class InvalidTokenException(RootException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message="Unable to validate token credential",
        )


class InvalidCredentialException(RootException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message="Unable to validate credential",
        )


class RoleNotGrantedException(RootException):
    def __init__(self, expected_roles: Iterable[str]):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            message=f"Role not granted. Required: {expected_roles}",
        )
