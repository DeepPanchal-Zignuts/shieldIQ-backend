from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ViewSet

from apps.campaigns.serializers.campaign_serializer import (
    CreateCampaignRequestSerializer,
    CreateCampaignResponseSerializer,
    CampaignListResponseSerializer,
    GetCampaignResponseSerializer,
)
from apps.campaigns.services.campaign_service import CampaignService
from common.constants.messages import CampaignMessages
from common.responses.api_response import ApiResponse


class CampaignController(ViewSet):
    permission_classes = [IsAdminUser]

    # POST /api/v1/admin/campaign/
    def create(self, request):

        # Validate request
        serializer = CreateCampaignRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Create the campaign
        new_campaign = CampaignService.create_campaign(
            data=serializer.validated_data,
            user=request.user,
        )

        # Serialize the response data
        response_data = CreateCampaignResponseSerializer(
            {"campaign": new_campaign["campaign"]}
        )

        return ApiResponse.created(
            data=response_data.data,
            message=CampaignMessages.CAMPAIGN_CREATED,
        )

    # GET /api/v1/admin/campaign/
    def list(self, request):
        # Create the campaign
        campaigns_list = CampaignService.get_all_campaigns(
            user_id=request.user.id,
        )

        # Serialize the response data
        response_data = CampaignListResponseSerializer(campaigns_list)

        return ApiResponse.success(
            data=response_data.data,
            message=CampaignMessages.CAMPAIGNS_FETCHED,
        )

    # GET /api/v1/admin/campaign/{campaign_id}/
    def retrieve(self, request, pk=None):

        campaign = CampaignService.get_campaign_details(campaign_id=pk)

        # Serialize the response data
        response_data = GetCampaignResponseSerializer(campaign)

        return ApiResponse.success(
            data=response_data.data,
            message=CampaignMessages.CAMPAIGN_FETCHED,
        )
