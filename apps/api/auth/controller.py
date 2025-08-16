from typing import Annotated

from apps.api.auth.dto.request import SigninRequest
from apps.api.auth.dto.response import TokenResponse
from apps.api.auth.service import AuthService
from apps.api.user.service import UserService
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter
from fastapi.params import Depends

from apps.api.user.dto.request import CreateUser
from apps.api.user.dto.response import UserResponse
from apps.containers import Application

auth_router = APIRouter(
    prefix="/auth",
    tags=["Auth Module"],
)


@auth_router.post("/signup", summary="Create user", response_model=UserResponse)
@inject
async def signup(
    body: CreateUser,
    user_service: Annotated[UserService, Depends(Provide[Application.user.service])],
):
    user = await user_service.create_user(body)
    return user


@auth_router.post("/signin", response_model=TokenResponse)
@inject
async def signin(
    body: SigninRequest,
    service: Annotated[AuthService, Depends(Provide[Application.auth.service])],
):
    print(service)
    token = await service.signin(body)
    return {
        "access_token": token,
    }
