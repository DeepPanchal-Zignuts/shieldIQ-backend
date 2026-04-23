from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ViewSet

from apps.campaigns.serializers.campaign_serializer import (
    DashboardResponseSerializer,
)
from apps.events.services.campaign_stats_service import CampaignStatsService
from common.constants.messages import CampaignMessages, DashboardMeessages
from common.responses.api_response import ApiResponse


class CampaignStatsController(ViewSet):

    # GET /api/v1/admin/stats/
    def list(self, request):
        # find the admin dashboard
        admin_dashboard_data = CampaignStatsService.get_admin_dashboard()

        # Serialize the response data
        response_data = DashboardResponseSerializer({"stats": admin_dashboard_data})

        return ApiResponse.success(
            data=response_data.data,
            message=DashboardMeessages.DASHBOARD_DATA_FETCHED,
        )
