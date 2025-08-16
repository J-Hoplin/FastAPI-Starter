import jwt

from apps.core.database.models import User
from datetime import datetime, timedelta, timezone


def create_access_token(
    user: User, jwt_secret_key: str, jwt_expire_minute: int, jwt_algorithm: str
) -> str:
    # Warning: PyJWT Required Timezone Aware datetime object
    token_issued_at = datetime.now(timezone.utc)
    token_expires_at = token_issued_at + timedelta(minutes=jwt_expire_minute)

    payload = {
        "sub": user.username,
        "exp": token_expires_at,
        "iat": token_issued_at,
    }

    return jwt.encode(payload, jwt_secret_key, algorithm=jwt_algorithm)
