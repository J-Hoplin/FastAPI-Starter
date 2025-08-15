from fastapi import APIRouter

auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

@auth_router.post("/signup")
async def signup():
    ...


@auth_router.post("/signin")
async def signin():
    ...