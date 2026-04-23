from uuid import UUID

from django.db.models import Prefetch
from apps.campaigns.models.campaign_email_model import CampaignEmails
from apps.campaigns.models.campaign_model import Campaigns
from common.constants.error_code import ErrorCodes
from common.constants.messages import CampaignMessages
from common.exceptions.custom_exceptions import NotFoundException
from utils import date_utils


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

    @classmethod
    def update_campaign(campaign_id: UUID, data: dict) -> Campaigns:
        # Find the campaign to update
        campaign = CampaignRepository.get_campaign_by_id(campaign_id)

        # Update the campaign fields
        for field, value in data.items():
            setattr(campaign, field, value)

        # Save the campaign
        campaign.save()

        return campaign

    @classmethod
    def delete_campaign(campaign_id: UUID) -> None:
        # Find the campaign to delete
        campaign = CampaignRepository.get_campaign_by_id(campaign_id)

        # set the is_deleted flag to True for soft deletion and update the deleted_at time to current time.
        campaign.is_deleted = True
        campaign.deleted_at = date_utils.get_now()

        # Save the campaign
        campaign.save()
