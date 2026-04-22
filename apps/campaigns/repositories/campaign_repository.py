from uuid import UUID

from django.db.models import Prefetch
from apps.campaigns.models.campaign_email_model import CampaignEmails
from apps.campaigns.models.campaign_model import Campaigns
from common.constants.error_code import ErrorCodes
from common.constants.messages import CampaignMessages
from common.exceptions.custom_exceptions import NotFoundException


class CampaignRepository:

    @classmethod
    def create_campaign(cls, data: dict) -> Campaigns:
        return Campaigns.objects.create(**data)

    @classmethod
    def get_campaign_by_id(
        cls,
        campaign_id: UUID,
    ) -> Campaigns:
        data = {
            "id": campaign_id,
            "is_deleted": False,
        }
        try:
            return Campaigns.objects.get(**data)
        except Campaigns.DoesNotExist as e:
            raise NotFoundException(
                message=str(e),
                error_code=ErrorCodes.NOT_FOUND,
            )

    @classmethod
    def get_campaigns_by_user_id(cls, user_id: UUID):
        return Campaigns.objects.filter(
            created_by=user_id,
            is_deleted=False,
        ).order_by("-created_at")

    @classmethod
    def get_campaign_with_emails(cls, campaign_id):
        campaign = (
            Campaigns.objects.filter(
                id=campaign_id,
                is_deleted=False,
            )
            .prefetch_related(
                Prefetch(
                    "emails",
                    queryset=CampaignEmails.objects.filter(is_deleted=False).order_by(
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
