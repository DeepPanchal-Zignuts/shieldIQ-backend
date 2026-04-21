from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ViewSet

from apps.events.serializers.campaign_event_serializer import (
    CreateCampaignEventRequestSerializer,
    CampaignEventResponseSerializer,
)
from apps.campaigns.services.campaign_email_service import CampaignEmailService
from apps.events.services.campaign_event_service import CampaignEventService
from common.constants.messages import CampaignMessages
from common.responses.api_response import ApiResponse


class CampaignEventsController(ViewSet):
    # POST /api/v1/events/track
    @action(
        detail=False,
        methods=["post"],
        url_path="track",
        url_name="track",
        permission_classes=[IsAuthenticated],
    )
    def create_campaign_event(self, request):

        # Validate request
        serializer = CreateCampaignEventRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Create the campaign event
        new_event = CampaignEventService.create_campaign_event(
            campaign_id=serializer.validated_data["campaign_id"],
            campaign_email_id=serializer.validated_data["campaign_email_id"],
            user=request.user,
            event_type=serializer.validated_data["event_type"],
        )

        # Serialize the response data
        response_data = CampaignEventResponseSerializer({"event": new_event["event"]})

        return ApiResponse.created(
            data=response_data.data,
            message=CampaignMessages.CAMPAIGN_EVENT_CREATED,
        )
