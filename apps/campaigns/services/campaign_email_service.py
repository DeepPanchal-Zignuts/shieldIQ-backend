from uuid import UUID
from apps.campaigns.repositories.campaign_email_repository import (
    CampaignEmailRepository,
)
from apps.campaigns.repositories.campaign_repository import CampaignRepository


class CampaignEmailService:

    @staticmethod
    def create_campaign_email(data: dict, campaign_id) -> dict:
        campaign = CampaignRepository.get_campaign_by_id(campaign_id)
        data["campaign"] = campaign

        campaign_email = CampaignEmailRepository.create_campaign_email(data)

        return {
            "campaign_email": campaign_email,
        }

    @staticmethod
    def get_user_campaign_emails(user_id: UUID, filters: dict) -> dict:
        return CampaignRepository.get_user_campaign_emails(user_id, filters)
