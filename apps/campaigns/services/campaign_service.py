from apps.campaigns.repositories.campaign_repository import CampaignRepository
from apps.campaigns.repositories.campaign_email_repository import (
    CampaignEmailRepository,
)
from common.constants.email_templates import DEFAULT_CAMPAIGN_EMAILS


class CampaignService:

    @staticmethod
    def create_campaign(data: dict, user) -> dict:
        data["created_by"] = user
        create_default_emails = data.pop("create_default_emails", False)

        # Create the campaign in the database
        campaign = CampaignRepository.create_campaign(data)

        # If user wants default emails, create them.
        if create_default_emails:
            # Create each default email
            for template in DEFAULT_CAMPAIGN_EMAILS:
                email_data = {
                    "campaign": campaign,
                    **template,
                }
                CampaignEmailRepository.create_campaign_email(email_data)

        return {
            "campaign": campaign,
        }
