from apps.campaigns.models.campaign_model import Campaign


class CampaignRepository:

    @classmethod
    def create_campaign(cls, data: dict) -> Campaign:
        return Campaign.objects.create(**data)
