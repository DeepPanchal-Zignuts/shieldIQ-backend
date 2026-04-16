import time
import jwt
from apps.users.repositories.user_repository import UserRepository
from config import settings
from common.constants.messages import UserMessages, AuthMessages


# generate_access_token generates access token for user
def generate_access_token(user) -> str:
    now = int(time.time())
    exp_ms = now + int(settings.ACCESS_TOKEN_LIFETIME.total_seconds())

    payload = {
        "user_id": str(user.id),
        "email": user.email,
        "iat": now,
        "exp": exp_ms,
    }

    return jwt.encode(
        payload,
        settings.ACCESS_SECRET_KEY,
        algorithm=settings.TOKEN_ALGORITHM,
    )


# generate_refresh_token generates refresh token for user
def generate_refresh_token(user) -> str:

    now = int(time.time())
    exp_ms = now + int(settings.REFRESH_TOKEN_LIFETIME.total_seconds())

    payload = {
        "user_id": str(user.id),
        "email": user.email,
        "iat": now,
        "exp": exp_ms,
    }

    return jwt.encode(
        payload, settings.REFRESH_SECRET_KEY, algorithm=settings.TOKEN_ALGORITHM
    )


# verify_token verifies the authenticity of a JWT token
def verify_token(token: str, secret_key: str) -> dict:
    try:
        # Decode the JWT token with incoming secret
        payload = jwt.decode(token, secret_key, algorithms=[settings.TOKEN_ALGORITHM])

        # Check if the user exists
        user = UserRepository.get_by_email(email=payload["email"])
        if not user:
            return {"valid": False, "error": UserMessages.USER_NOT_FOUND}

        return {"valid": True, "user": user, "payload": payload}
    except jwt.ExpiredSignatureError:
        return {"valid": False, "error": AuthMessages.TOKEN_EXPIRED}
    except jwt.InvalidTokenError as e:
        return {"valid": False, "error": AuthMessages.INVALID_TOKEN}
