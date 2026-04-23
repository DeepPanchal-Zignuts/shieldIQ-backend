from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ViewSet

from apps.campaigns.serializers.campaign_serializer import (
    CreateCampaignRequestSerializer,
    CreateCampaignResponseSerializer,
    CampaignListResponseSerializer,
    GetCampaignResponseSerializer,
    UpdateCampaignRequestSerializer,
)
from apps.campaigns.services.campaign_service import CampaignService
from common.constants.messages import CampaignMessages
from common.responses.api_response import ApiResponse


class CampaignController(ViewSet):
    permission_classes = [IsAdminUser]

    # POST /api/v1/admin/campaigns/
    def create(self, request):
        serializer = CreateCampaignRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_campaign = CampaignService.create_campaign(
            data=serializer.validated_data,
            user=request.user,
        )

        response_data = CreateCampaignResponseSerializer(
            {"campaign": new_campaign["campaign"]}
        )

        return ApiResponse.created(
            data=response_data.data,
            message=CampaignMessages.CAMPAIGN_CREATED,
        )

    # GET /api/v1/admin/campaigns/
    def list(self, request):
        campaigns_list = CampaignService.get_all_campaigns(
            user_id=request.user.id,
        )

        response_data = CampaignListResponseSerializer(campaigns_list)

        return ApiResponse.success(
            data=response_data.data,
            message=CampaignMessages.CAMPAIGNS_FETCHED,
        )

    # GET /api/v1/admin/campaign/{pk}/
    def retrieve(self, request, pk=None):
        campaign = CampaignService.get_campaign_details(campaign_id=pk)

        response_data = GetCampaignResponseSerializer(campaign)

        return ApiResponse.success(
            data=response_data.data,
            message=CampaignMessages.CAMPAIGN_FETCHED,
        )

    # PATCH /api/v1/admin/campaign/{pk}/
    def partial_update(self, request, pk=None):
        serializer = UpdateCampaignRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        updated_campaign = CampaignService.update_campaign(
            campaign_id=pk,
            data=serializer.validated_data,
        )

        response_data = CreateCampaignResponseSerializer(
            {"campaign": updated_campaign["campaign"]}
        )

        return ApiResponse.success(
            data=response_data.data,
            message=CampaignMessages.CAMPAIGN_UPDATED,
        )

    # DELETE /api/v1/admin/campaign/{pk}/
    def destroy(self, request, pk=None):
        CampaignService.delete_campaign(campaign_id=pk)

        return ApiResponse.success(
            message=CampaignMessages.CAMPAIGN_DELETED,
        )
