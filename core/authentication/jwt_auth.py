from rest_framework.authentication import BaseAuthentication
from common.exceptions.custom_exceptions import (
    UnauthorizedException,
)
from common.constants.messages import AuthMessages, PermissionMessages
from common.constants.error_code import ErrorCodes
from config import settings
from utils.token_utils import verify_token


# JWTAuthentication is responsible to authenticate incoming requests.
class JWTAuthentication(BaseAuthentication):

    keyword = "Bearer"

    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")

        # 1. No header → return None (important)
        if not auth_header:
            return None
        parts = auth_header.split()

        # 2. Invalid format → raise error
        if len(parts) != 2 or parts[0] != self.keyword:
            raise UnauthorizedException(
                message=PermissionMessages.AUTH_CREDS_INVALID,
                error_code=ErrorCodes.INVALID_TOKEN,
            )
        raw_token = parts[1]

        # 3. Verify token
        decoded_token_data = verify_token(raw_token, settings.ACCESS_SECRET_KEY)
        if not decoded_token_data["valid"]:
            raise UnauthorizedException(
                message=decoded_token_data["error"],
                error_code=ErrorCodes.INVALID_TOKEN,
            )

        # 4. Optional checks
        user = decoded_token_data.get("user")
        if not user.is_active:
            raise UnauthorizedException(
                message=AuthMessages.ACCOUNT_DEACTIVATED,
                error_code=ErrorCodes.ACCOUNT_DEACTIVATED,
            )

        # 5. Return user and token
        return (user, raw_token)
