"""
Centralised API response helpers.
Every controller should return responses through this utility so the
frontend always receives a consistent envelope.

Standard shape:
{
    "success": true | false,
    "message": "...",
    "data": { ... } | null,
    "errors": { ... } | null,
    "error_code": "..." | null,
    "meta": { ... } | null
}
"""

from rest_framework.response import Response
from rest_framework import status as http_status


class ApiResponse:
    """
    Static helper class to build standardised DRF Response objects.
    """

    @staticmethod
    def success(
        data=None,
        message: str = "Success",
        status_code: int = http_status.HTTP_200_OK,
        meta: dict = None,
    ) -> Response:
        payload = {
            "success": True,
            "message": message,
            "data": data,
            "errors": None,
            "error_code": None,
            "meta": meta,
        }
        return Response(payload, status=status_code)

    @staticmethod
    def created(
        data=None,
        message: str = "Resource created successfully.",
    ) -> Response:
        return ApiResponse.success(
            data=data,
            message=message,
            status_code=http_status.HTTP_201_CREATED,
        )

    @staticmethod
    def no_content(message: str = "Resource deleted successfully.") -> Response:
        payload = {
            "success": True,
            "message": message,
            "data": None,
            "errors": None,
            "error_code": None,
            "meta": None,
        }
        return Response(payload, status=http_status.HTTP_200_OK)

    @staticmethod
    def error(
        message: str = "An error occurred.",
        error_code: str = "ERROR",
        errors=None,
        status_code: int = http_status.HTTP_400_BAD_REQUEST,
    ) -> Response:
        payload = {
            "success": False,
            "message": message,
            "data": None,
            "errors": errors,
            "error_code": error_code,
            "meta": None,
        }
        return Response(payload, status=status_code)

    @staticmethod
    def paginated(
        data,
        message: str = "Success",
        page: int = 1,
        page_size: int = 20,
        total_count: int = 0,
    ) -> Response:
        payload = {
            "success": True,
            "message": message,
            "data": data,
            "errors": None,
            "error_code": None,
            "meta": {
                "page": page,
                "page_size": page_size,
                "total_count": total_count,
                "total_pages": (
                    (total_count + page_size - 1) // page_size if page_size else 0
                ),
            },
        }
        return Response(payload, status=http_status.HTTP_200_OK)
