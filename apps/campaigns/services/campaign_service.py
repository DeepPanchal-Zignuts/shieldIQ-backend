from apps.campaigns.repositories.campaign_repository import CampaignRepository


class CampaignService:

    @staticmethod
    def create_campaign(data: dict, user) -> dict:
        data["created_by"] = user

        campaign = CampaignRepository.create_campaign(data)

        return {
            "campaign": campaign,
        }
