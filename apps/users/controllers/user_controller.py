from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from apps.users.serializers.user_serializer import (
    UserListRequestSerializer,
    UserListResponseSerializer,
    UserDetailsWithStatsResponseSerializer,
    UserProfileDetailsResponseSerializer,
)
from apps.users.services.user_service import UserService
from common.responses.api_response import ApiResponse
from common.constants.messages import UserMessages


class UserController(ViewSet):

    # GET /api/v1/users/me/
    @action(
        detail=False,
        methods=["get"],
        url_path="me",
        url_name="me",
    )
    def get_user_profile_details(self, request):

        # Get the user profile details
        user_data = UserService.get_profile_details(
            user_id=request.user.id,
        )

        # Serialize the response data
        response_data = UserProfileDetailsResponseSerializer(
            {
                "user": user_data["user"],
            }
        )

        return ApiResponse.success(
            data=response_data.data,
            message=UserMessages.USER_PROFILE_SUCCESS,
        )

    # GET /api/v1/admin/users/list
    @action(
        detail=False,
        methods=["get"],
        url_path="list",
        url_name="list",
    )
    def get_all_users(self, request):
        # Validate the request data
        serializer = UserListRequestSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        # Get the user profile details
        all_users = UserService.get_all_users(
            filters=serializer.validated_data,
        )

        # Serialize the response data
        response_data = UserListResponseSerializer(
            {
                "users": all_users["users"],
            }
        )

        return ApiResponse.success(
            data=response_data.data,
            message=UserMessages.USERS_FETCH_SUCCESS,
        )

    # GET /api/v1/admin/users/{user_id}/
    def retrieve(self, request, pk=None):
        # Get the user profile details
        user_details = UserService.get_user_details(user_id=pk)

        # Serialize the response data
        response_data = UserDetailsWithStatsResponseSerializer(user_details)

        return ApiResponse.success(
            data=response_data.data,
            message=UserMessages.USER_PROFILE_SUCCESS,
        )
