from apps.core.exception.base import RootException
from typing import List
from fastapi import status


class CredentialAlreadyExistException(RootException):
    def __init__(self, conflict_clauses: List[str]):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="Credential already taken: {}".format(
                " and ".join(conflict_clauses)
            ),
        )
