from typing import Union, Dict
from fastapi import Request
from fastapi.responses import JSONResponse


"""
Root Exception class

Require
    - status_code
    - message
"""


class RootException(Exception):
    def __init__(self, status_code: int, message: str = Union[str, object, Dict]):
        self.status_code = status_code
        self.message = message


"""
Root Exception Handler
"""


async def root_exception_handler(request: Request, exc: RootException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})
