from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter
from fastapi.params import Depends, Query, Path

from apps.api.user.dto.request import ListUserFilter
from apps.api.user.dto.response import UserResponse
from apps.api.user.service import UserService
from apps.containers import Application
from apps.core.common.response import PaginatedResponse
from apps.core.database.models import User
from apps.core.auth.context import role_granted_user, get_authenticated_user

user_router = APIRouter(
    prefix="/user", tags=["User Module"], dependencies=[Depends(get_authenticated_user)]
)

TUserService = Annotated[UserService, Depends(Provide[Application.user.service])]


@user_router.get(
    path="/", summary="List users", response_model=PaginatedResponse[UserResponse]
)
@inject
async def list_user(
    qs: Annotated[ListUserFilter, Query()],
    service: TUserService,
    user: Annotated[User, Depends(role_granted_user(["superuser", "staff"]))],
):
    total, users = await service.list_user(qs)
    return PaginatedResponse(total=total, items=users)


@user_router.get(
    path="/{user_id}", summary="Get user with user id", response_model=UserResponse
)
@inject
async def retrieve_user(
    user_id: Annotated[int, Path()],
    service: TUserService,
):
    return await service.retrieve_user(user_id)
