import os
import secrets
from typing import Annotated

from fastapi import APIRouter, status, HTTPException
from fastapi.params import Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.openapi.docs import get_swagger_ui_html

security = HTTPBasic()

document_router = APIRouter(
    prefix="/docs",

)

@document_router.get(
    path="/swagger",
    include_in_schema=False
)
def swagger_auth(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    typed_username = credentials.username
    typed_userpassword = credentials.password

    expected_username = os.getenv("SWAGGER_USERNAME")
    expected_userpassword = os.getenv("SWAGGER_PASSWORD")

    is_username_correct = secrets.compare_digest(typed_username, expected_username)
    is_password_correct = secrets.compare_digest(typed_userpassword, expected_userpassword)
    if not (is_username_correct and is_password_correct):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return get_swagger_ui_html(openapi_url="/docs/openapi.json", title="Swagger UI")
