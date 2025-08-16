from apps.core.exception.base import RootException
from fastapi import status


class CredentialAlreadyExist(RootException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST, message="Credential already taken"
        )
