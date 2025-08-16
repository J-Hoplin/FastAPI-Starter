from typing import Any

from starlette.requests import Request

from apps.core.auth.hash import hash_password
from apps.core.database.models import User
from sqladmin import ModelView


class UserAdmin(ModelView, model=User):
    column_list = [
        User.id,
        User.email,
        User.username,
        User.is_active,
        User.is_staff,
        User.is_superuser,
    ]
    column_labels = {User.hashed_password: "password"}

    async def on_model_change(
        self, data: dict, model: Any, is_created: bool, request: Request
    ) -> None:
        raw_password = data.get("hashed_password")
        if is_created:
            if raw_password:
                data["hashed_password"] = hash_password(raw_password)
            data["is_active"] = True
        else:
            if raw_password:
                data["hashed_password"] = hash_password(raw_password)
            else:
                data.pop("hashed_password")
