from rest_framework import serializers
from apps.campaigns.models.campaign_model import Campaign
from common.constants import constants
from common.constants import messages
from common.constants.messages import CampaignMessages
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
    create_default_emails = serializers.BooleanField(default=False)

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


class CreateCampaignEmailRequestSerializer(serializers.Serializer):
    sender = serializers.CharField(
        required=True,
        min_length=3,
        max_length=255,
    )
    from_email = serializers.EmailField(
        required=True,
        min_length=3,
        max_length=255,
    )
    subject = serializers.CharField(
        required=True,
        min_length=3,
        max_length=255,
    )
    body = serializers.CharField()
    link_text = serializers.CharField(
        allow_blank=True,
        max_length=255,
    )
    is_phishing = serializers.BooleanField(default=False)


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


class CampaignEmailResponseSerializer(serializers.Serializer):
    """Serializes user data for API responses."""

    id = serializers.UUIDField()
    sender = serializers.CharField()
    from_email = serializers.EmailField()
    subject = serializers.CharField()
    body = serializers.CharField()
    link_text = serializers.CharField()
    is_phishing = serializers.BooleanField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()


class CreateCampaignResponseSerializer(serializers.Serializer):
    campaign = CampaignResponseSerializer()


class CreateCampaignEmailResponseSerializer(serializers.Serializer):
    campaign_email = CampaignEmailResponseSerializer()


class CampaignStatsSerializer(serializers.Serializer):
    average_score_change = serializers.FloatField()
    click_rate = serializers.FloatField()
    report_rate = serializers.FloatField()
    progress_rate = serializers.FloatField()


class CampaignWithStatsSerializer(serializers.Serializer):
    campaign = CampaignResponseSerializer()
    stats = CampaignStatsSerializer()


class CampaignListResponseSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    campaigns = CampaignWithStatsSerializer(many=True)


class GetCampaignResponseSerializer(serializers.ModelSerializer):
    emails = CampaignEmailResponseSerializer(many=True)

    class Meta:
        model = Campaign
        fields = [
            "id",
            "title",
            "description",
            "email_type",
            "status",
            "target_departments",
            "created_by",
            "start_date",
            "end_date",
            "emails",
        ]
