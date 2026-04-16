"""
Global DRF exception handler.
Intercepts all exceptions and returns a standardised JSON response.
"""

import logging

from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.exceptions import APIException, ValidationError
from django.http import Http404
from django.core.exceptions import PermissionDenied

from common.exceptions.custom_exceptions import BaseAPIException
from common.responses.api_response import ApiResponse
from common.constants import error_code, messages

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    Custom exception handler that wraps all errors into the standardised
    ApiResponse format.
    """

    # ── Handle our custom exceptions first ──────────────────
    if isinstance(exc, BaseAPIException):
        logger.warning(
            "Custom API exception: %s | code=%s | details=%s",
            exc.message,
            exc.error_code,
            exc.details,
        )
        return ApiResponse.error(
            message=exc.message,
            error_code=exc.error_code,
            errors=exc.details if exc.details else None,
            status_code=exc.status_code,
        )

    # ── Let DRF handle its own exceptions ────────────────────
    response = drf_exception_handler(exc, context)

    if response is not None:
        # DRF ValidationError
        if isinstance(exc, ValidationError):
            return ApiResponse.error(
                message=messages.ValidationMessages.VALIDATION_FAILED,
                error_code=error_code.ErrorCodes.VALIDATION_ERROR,
                errors=response.data,
                status_code=response.status_code,
            )

        # Other DRF APIException subclasses
        if isinstance(exc, APIException):
            detail = exc.detail if hasattr(exc, "detail") else str(exc)
            return ApiResponse.error(
                message=str(detail),
                error_code=(
                    exc.default_code if hasattr(exc, "default_code") else "API_ERROR"
                ),
                status_code=response.status_code,
            )

    # ── Django 404 ───────────────────────────────────────────
    if isinstance(exc, Http404):
        return ApiResponse.error(
            message=messages.BaseMessages.NOT_FOUND,
            error_code=error_code.ErrorCodes.NOT_FOUND,
            status_code=404,
        )

    # ── Django PermissionDenied ──────────────────────────────
    if isinstance(exc, PermissionDenied):
        return ApiResponse.error(
            message=messages.PermissionMessages.PERMISSION_DENIED,
            error_code=error_code.ErrorCodes.FORBIDDEN,
            status_code=403,
        )

    # ── Catch-all for unhandled exceptions ───────────────────
    logger.exception("Unhandled exception: %s", exc)
    return ApiResponse.error(
        message=messages.BaseMessages.INTERNAL_SERVER_ERROR,
        error_code=error_code.ErrorCodes.INTERNAL_SERVER_ERROR,
        status_code=500,
    )
