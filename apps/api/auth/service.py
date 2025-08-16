from apps.api.auth.dto.request import SigninRequest
from apps.api.user.repository import UserRepository
from apps.core.auth.exception import InvalidCredentialException
from apps.core.auth.hash import verify_password
from apps.core.auth.token import create_access_token


class AuthService:
    def __init__(self, user_repository: UserRepository, config: dict):
        self.user_repository = user_repository
        self.config = config

    async def signin(self, body: SigninRequest):
        user = await self.user_repository.retrieve_user_with_unique_clause(
            key="email", value=body.email, filter_is_active=True
        )
        if not user:
            raise InvalidCredentialException()

        if not verify_password(body.password, user.hashed_password):
            raise InvalidCredentialException()

        token = create_access_token(
            user,
            self.config.get("JWT_SECRET_KEY"),
            self.config.get("JWT_EXPIRE_MINUTE"),
            self.config.get("JWT_ALGORITHM"),
        )
        return token
