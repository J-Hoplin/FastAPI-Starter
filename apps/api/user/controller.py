from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter
from fastapi.params import Depends, Query, Path

from apps.api.user.dto.request import ListUserFilter, CreateUser
from apps.api.user.dto.response import UserResponse
from apps.api.user.service import UserService
from apps.containers import Application
from apps.core.common.response import PaginatedResponse

user_router = APIRouter(prefix="/user", tags=["user"])


@user_router.get(
    path="/", summary="List users", response_model=PaginatedResponse[UserResponse]
)
@inject
async def list_user(
    qs: Annotated[ListUserFilter, Query()],
    service: UserService = Depends(Provide[Application.user.service]),
):
    total, users = await service.list_user(qs)
    return PaginatedResponse(total=total, items=users)


@user_router.get(
    path="/{user_id}", summary="Get user with user id", response_model=UserResponse
)
@inject
async def retrieve_user(
    user_id: Annotated[int, Path()],
    service: UserService = Depends(Provide[Application.user.service]),
):
    return await service.retrieve_user(user_id)


@user_router.post(path="/", summary="Create user", response_model=UserResponse)
@inject
async def create_user(
    body: CreateUser,
    service: UserService = Depends(Provide[Application.user.service]),
):
    user = await service.create_user(body)
    return user
