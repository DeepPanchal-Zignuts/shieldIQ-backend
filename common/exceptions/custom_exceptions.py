"""
Custom exception classes.
Provide domain-specific exceptions with HTTP status codes and error codes
so the global exception handler can build consistent API responses.
"""

from rest_framework import status
from common.constants import error_code, messages


class BaseAPIException(Exception):
    """
    Base exception for all custom API errors.
    Subclass this to create domain-specific exceptions.
    """

    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_message = messages.BaseMessages.INTERNAL_SERVER_ERROR
    default_error_code = error_code.ErrorCodes.INTERNAL_SERVER_ERROR

    def __init__(
        self, message: str = None, error_code: str = None, details: dict = None
    ):
        self.message = message or self.default_message
        self.error_code = error_code or self.default_error_code
        self.details = details or {}
        super().__init__(self.message)


# ──────────────────────────────────────────────────────────────
# 400-level exceptions
# ──────────────────────────────────────────────────────────────
class BadRequestException(BaseAPIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_message = messages.BaseMessages.BAD_REQUEST
    default_error_code = error_code.ErrorCodes.BAD_REQUEST


class ValidationException(BaseAPIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_message = messages.ValidationMessages.VALIDATION_FAILED
    default_error_code = error_code.ErrorCodes.VALIDATION_ERROR


class UnauthorizedException(BaseAPIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_message = messages.PermissionMessages.AUTH_CREDS_INVALID
    default_error_code = error_code.ErrorCodes.UNAUTHORIZED


class ForbiddenException(BaseAPIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_message = messages.PermissionMessages.PERMISSION_DENIED
    default_error_code = error_code.ErrorCodes.FORBIDDEN


class NotFoundException(BaseAPIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_message = messages.BaseMessages.NOT_FOUND
    default_error_code = error_code.ErrorCodes.NOT_FOUND


class ConflictException(BaseAPIException):
    status_code = status.HTTP_409_CONFLICT
    default_message = messages.BaseMessages.CONFLICT
    default_error_code = error_code.ErrorCodes.CONFLICT


class TooManyRequestsException(BaseAPIException):
    status_code = status.HTTP_429_TOO_MANY_REQUESTS
    default_message = messages.BaseMessages.RATE_LIMIT_EXCEEDED
    default_error_code = error_code.ErrorCodes.RATE_LIMIT_EXCEEDED


# ──────────────────────────────────────────────────────────────
# 500-level exceptions
# ──────────────────────────────────────────────────────────────
class InternalServerErrorException(BaseAPIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_message = messages.BaseMessages.INTERNAL_SERVER_ERROR
    default_error_code = error_code.ErrorCodes.INTERNAL_SERVER_ERROR


class ServiceUnavailableException(BaseAPIException):
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    default_message = messages.BaseMessages.SERVICE_UNAVAILABLE
    default_error_code = error_code.ErrorCodes.SERVICE_UNAVAILABLE
