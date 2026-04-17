from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ViewSet
from apps.users.serializers.user_serializer import (
    UserProfileDetailsResponseSerializer,
)
from apps.users.services.profile_service import ProfileService
from common.responses.api_response import ApiResponse
from common.constants.messages import UserMessages


class ProfileController(ViewSet):

    # GET /api/v1/profile/me/
    @action(
        detail=False,
        methods=["get"],
        url_path="me",
        url_name="me",
        permission_classes=[IsAuthenticated],
    )
    def get_user_profile_details(self, request):

        # Get the user profile details
        user_data = ProfileService.get_profile_details(
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
