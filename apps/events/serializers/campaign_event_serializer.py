from rest_framework import serializers
from common.constants.constants import CampaignEventsEnum

# ══════════════════════════════════════════════════════════════
# Request Serializers (input validation)
# ══════════════════════════════════════════════════════════════


class CreateCampaignEventRequestSerializer(serializers.Serializer):
    campaign_id = serializers.UUIDField(required=True)
    campaign_email_id = serializers.UUIDField(required=True)
    event_type = serializers.ChoiceField(
        required=True,
        choices=CampaignEventsEnum.choices,
    )


# ══════════════════════════════════════════════════════════════
# Response Serializers (output formatting)
# ══════════════════════════════════════════════════════════════


class CampaignEventResponse(serializers.Serializer):
    id = serializers.UUIDField()
    campaign = serializers.CharField()
    campaign_email = serializers.CharField()
    user = serializers.CharField()
    event_type = serializers.ChoiceField(choices=CampaignEventsEnum.choices)
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()


class CampaignEventResponseSerializer(serializers.Serializer):
    event = CampaignEventResponse()
