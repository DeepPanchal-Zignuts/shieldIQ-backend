from uuid import UUID
from apps.campaigns.models.campaign_model import Campaign
from common.constants.error_code import ErrorCodes
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
