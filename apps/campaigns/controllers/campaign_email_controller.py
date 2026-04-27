from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ViewSet

from apps.campaigns.serializers.campaign_serializer import (
    CreateCampaignEmailRequestSerializer,
    CreateCampaignEmailResponseSerializer,
    UserSimulationEmailSerializer,
    SimulationCampaignSerializer,
)
from apps.campaigns.services.campaign_email_service import CampaignEmailService
from common.constants.messages import CampaignMessages
from common.responses.api_response import ApiResponse


class CampaignEmailController(ViewSet):
    # POST /api/v1/campaigns/{campaign_id}/emails/
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

    # GET /api/v1/users/simulation/
    def list(self, request):
        filters = {
            "search": request.query_params.get("search"),
            "campaign_id": request.query_params.get("campaign_id"),
            "page": int(request.query_params.get("page", 1)),
            "page_size": int(request.query_params.get("page_size", 10)),
            "ordering": request.query_params.get("ordering", "-created_at"),
        }

        # Fetch all the simulation mails
        simulation_mails = CampaignEmailService.get_user_campaign_emails(
            user_id=request.user.id,
            filters=filters,
        )

        # Serialize the response data
        response_data = UserSimulationEmailSerializer(
            simulation_mails["results"], many=True
        )

        return ApiResponse.success(
            data={
                "count": simulation_mails["count"],
                "results": response_data.data,
            },
            message=CampaignMessages.SIMULATION_MAILS_FETCHED,
        )

    # GET /api/v1/users/simulation/campaigns/
    def list_simulation_campaigns(self, request):
        # Fetch the simulation campaigns for the user
        campaigns = CampaignEmailService.get_user_simulation_campaigns(
            user_id=request.user.id,
        )

        # Serialize the response data
        response_data = SimulationCampaignSerializer(campaigns, many=True)

        return ApiResponse.success(
            data=response_data.data,
            message=CampaignMessages.CAMPAIGNS_FETCHED,
        )
