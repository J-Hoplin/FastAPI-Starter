from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter
from fastapi.params import Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.openapi.docs import get_swagger_ui_html

from apps.api.auth.exception import PermissionDeniedException
from apps.api.user.repository import UserRepository
from apps.containers import Application
from apps.core.auth.exception import InvalidCredentialException
from apps.core.auth.hash import verify_password

security = HTTPBasic()

document_router = APIRouter(
    prefix="/docs",
)


@document_router.get(path="/swagger", include_in_schema=False)
@inject
async def swagger_auth(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
    user_repository: Annotated[
        UserRepository, Depends(Provide[Application.user.repository])
    ],
):
    typed_username = credentials.username
    typed_userpassword = credentials.password

    user = await user_repository.retrieve_superuser_or_staff(
        username=typed_username,
    )

    if not user:
        raise PermissionDeniedException()

    if not verify_password(typed_userpassword, user.hashed_password):
        raise InvalidCredentialException()

    return get_swagger_ui_html(
        openapi_url="/docs/openapi.json",
        title="Swagger UI",
        swagger_ui_parameters={
            "displayRequestDuration": True,
            "persistAuthorization": True,
        },
    )
