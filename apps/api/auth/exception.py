from apps.core.exception.base import RootException
from fastapi import status


class PermissionDeniedException(RootException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            message="Permission Denied. You do not have permission to do this action.",
        )
