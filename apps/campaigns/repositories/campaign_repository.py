from uuid import UUID
from apps.campaigns.models.campaign_model import Campaign


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

        return Campaign.objects.get(**data)
