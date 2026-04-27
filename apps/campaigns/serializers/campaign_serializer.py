from rest_framework import serializers
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


class UpdateCampaignRequestSerializer(serializers.Serializer):
    title = serializers.CharField(required=False, max_length=155)
    description = serializers.CharField(
        required=False, min_length=3, max_length=255, allow_blank=True
    )
    start_date = serializers.DateField(required=False)
    end_date = serializers.DateField(required=False)
    target_departments = serializers.ListField(
        child=serializers.CharField(), required=False
    )
    email_type = serializers.ChoiceField(
        choices=constants.CampaignEmailsEnum.choices, required=False
    )
    status = serializers.ChoiceField(
        choices=constants.CampaignStatusEnum.choices, required=False
    )

    def validate(self, attrs):
        start_date = attrs.get("start_date")
        end_date = attrs.get("end_date")
        if start_date and end_date and end_date <= start_date:
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
    average_score = serializers.FloatField()
    click_rate = serializers.FloatField()
    report_rate = serializers.FloatField()
    active_users = serializers.IntegerField()
    progress = serializers.DictField()


class CampaignWithStatsSerializer(serializers.Serializer):
    campaign = CampaignResponseSerializer()
    stats = CampaignStatsSerializer()


class CampaignListResponseSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    campaigns = CampaignWithStatsSerializer(many=True)


class GetCampaignResponseSerializer(serializers.Serializer):
    # flatten campaign fields
    id = serializers.UUIDField(source="campaign.id")
    title = serializers.CharField(source="campaign.title")
    description = serializers.CharField(source="campaign.description")
    email_type = serializers.CharField(source="campaign.email_type")
    status = serializers.CharField(source="campaign.status")
    target_departments = serializers.ListField(source="campaign.target_departments")
    created_by = serializers.CharField(source="campaign.created_by.email")
    start_date = serializers.DateField(source="campaign.start_date")
    end_date = serializers.DateField(source="campaign.end_date")

    emails = CampaignEmailResponseSerializer(source="campaign.emails.all", many=True)

    stats = CampaignStatsSerializer()


class DashboardResponseSerializer(serializers.Serializer):
    stats = CampaignStatsSerializer()


class UserSimulationEmailSerializer(serializers.Serializer):

    id = serializers.UUIDField()
    sender = serializers.CharField()
    from_email = serializers.EmailField()
    subject = serializers.CharField()
    body = serializers.CharField()
    link_text = serializers.CharField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
    campaign_id = serializers.UUIDField()
    is_user_interacted = serializers.BooleanField()


class SimulationCampaignSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    title = serializers.CharField()
    email_type = serializers.CharField()
    status = serializers.CharField()
