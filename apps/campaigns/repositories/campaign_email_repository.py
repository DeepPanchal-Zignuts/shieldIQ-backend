from uuid import UUID
from apps.campaigns.models.campaign_email_model import CampaignEmail


class CampaignEmailRepository:

    @classmethod
    def create_campaign_email(cls, data: dict) -> CampaignEmail:
        return CampaignEmail.objects.create(**data)
