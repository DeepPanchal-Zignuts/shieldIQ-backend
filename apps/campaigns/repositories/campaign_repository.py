from uuid import UUID

from django.db.models import Prefetch
from apps.campaigns.models.campaign_email_model import CampaignEmail
from apps.campaigns.models.campaign_model import Campaign
from common.constants.error_code import ErrorCodes
from common.constants.messages import CampaignMessages
from common.exceptions.custom_exceptions import NotFoundException


class CampaignRepository:

    @classmethod
    def create_campaign(cls, data: dict) -> Campaign:
        return Campaign.objects.create(**data)

    @classmethod
    def get_campaign_by_id(
        cls,
        campaign_id: UUID,
    ) -> Campaign:
        data = {
            "id": campaign_id,
            "is_deleted": False,
        }
        try:
            return Campaign.objects.get(**data)
        except Campaign.DoesNotExist as e:
            raise NotFoundException(
                message=str(e),
                error_code=ErrorCodes.NOT_FOUND,
            )

    @classmethod
    def get_campaigns_by_user_id(cls, user_id: UUID):
        return Campaign.objects.filter(
            created_by=user_id,
            is_deleted=False,
        ).order_by("-created_at")

    @classmethod
    def get_campaign_with_emails(cls, campaign_id):
        campaign = (
            Campaign.objects.filter(
                id=campaign_id,
                is_deleted=False,
            )
            .prefetch_related(
                Prefetch(
                    "emails",
                    queryset=CampaignEmail.objects.filter(is_deleted=False).order_by(
                        "created_at"
                    ),
                )
            )
            .first()
        )

        if not campaign:
            raise NotFoundException(
                message=CampaignMessages.CAMPAIGN_NOT_FOUND,
                error_code=ErrorCodes.NOT_FOUND,
            )

        return campaign
