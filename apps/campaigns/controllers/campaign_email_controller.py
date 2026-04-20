from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ViewSet

from apps.campaigns.serializers.campaign_serializer import (
    CreateCampaignEmailRequestSerializer,
    CreateCampaignEmailResponseSerializer,
)
from apps.campaigns.services.campaign_email_service import CampaignEmailService
from common.constants.messages import CampaignMessages
from common.responses.api_response import ApiResponse


class CampaignEmailController(ViewSet):
    # GET /api/v1/campaigns/{campaign_id}/emails/
    @action(
        detail=True,
        methods=["post"],
        url_path="emails",
        url_name="emails",
        permission_classes=[IsAdminUser],
    )
    def create_campaign_email(self, request, campaign_id=None):

        # Validate request
        serializer = CreateCampaignEmailRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Create the campaign email
        new_campaign = CampaignEmailService.create_campaign_email(
            data=serializer.validated_data,
            campaign_id=campaign_id,
        )

        # Serialize the response data
        response_data = CreateCampaignEmailResponseSerializer(
            {"campaign_email": new_campaign["campaign_email"]}
        )

        return ApiResponse.created(
            data=response_data.data,
            message=CampaignMessages.CAMPAIGN_EMAIL_CREATED,
        )
