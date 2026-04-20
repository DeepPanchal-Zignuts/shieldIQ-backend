from rest_framework import serializers
from common.constants import constants
from common.constants import messages
from common.constants.messages import CampaignMessages, ValidationMessages
from utils.date_utils import get_current_date

# ══════════════════════════════════════════════════════════════
# Request Serializers (input validation)
# ══════════════════════════════════════════════════════════════


class CreateCampaignRequestSerializer(serializers.Serializer):
    title = serializers.CharField(required=True, max_length=155)
    description = serializers.CharField(min_length=3, max_length=255, allow_blank=True)
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    target_departments = serializers.ListField(
        child=serializers.CharField(), required=False, default=[]
    )
    email_type = serializers.ChoiceField(choices=constants.CampaignEmailsEnum.choices)

    def validate(self, attrs):
        # Cross-field validation
        if attrs["start_date"] < get_current_date():
            raise serializers.ValidationError(
                CampaignMessages.START_DATE_GREATER_THAN_TODAY
            )
        if attrs["end_date"] <= attrs["start_date"]:
            raise serializers.ValidationError(
                messages.CampaignMessages.END_DATE_GREATER_THAN_START_DATE
            )

        return attrs


# ══════════════════════════════════════════════════════════════
# Response Serializers (output formatting)
# ══════════════════════════════════════════════════════════════


class CampaignResponseSerializer(serializers.Serializer):
    """Serializes user data for API responses."""

    id = serializers.UUIDField()
    title = serializers.CharField()
    description = serializers.CharField()
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    target_departments = serializers.ListField()
    email_type = serializers.ChoiceField(choices=constants.CampaignEmailsEnum.choices)
    status = serializers.ChoiceField(choices=constants.CampaignStatusEnum.choices)
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
    created_by = serializers.CharField()


class CreateCampaignResponseSerializer(serializers.Serializer):
    campaign = CampaignResponseSerializer()
