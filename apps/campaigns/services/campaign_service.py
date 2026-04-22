from uuid import UUID
from apps.campaigns.repositories.campaign_repository import CampaignRepository
from apps.campaigns.repositories.campaign_email_repository import (
    CampaignEmailRepository,
)
from apps.events.services.campaign_stats_service import CampaignStatsService
from common.constants.email_templates import DEFAULT_CAMPAIGN_EMAILS
from common.constants.error_code import ErrorCodes
from common.constants.messages import CampaignMessages
from common.exceptions.custom_exceptions import NotFoundException


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

    @staticmethod
    def get_all_campaigns(user_id: UUID) -> dict:
        # Get all campaigns for this user
        campaigns = CampaignRepository.get_campaigns_by_user_id(user_id)
        if not campaigns.exists():
            raise NotFoundException(
                message=CampaignMessages.NO_CAMPAIGNS_FOUND,
                error_code=ErrorCodes.NOT_FOUND,
            )

        return {
            "campaigns": campaigns,
            "count": campaigns.count(),
        }

    @staticmethod
    def get_all_campaigns(user_id: UUID) -> dict:
        # Get all campaigns for this user
        campaigns = CampaignRepository.get_campaigns_by_user_id(user_id)
        if not campaigns.exists():
            raise NotFoundException(
                message=CampaignMessages.NO_CAMPAIGNS_FOUND,
                error_code=ErrorCodes.NOT_FOUND,
            )

        # Create a list of the campaigns
        campaigns = list(campaigns)

        # For each campaign, get the stats and combine them
        enriched_campaigns = []
        for campaign in campaigns:
            stats = CampaignStatsService.get_campaign_stats(campaign.id)

            enriched_campaigns.append(
                {
                    "campaign": campaign,
                    "stats": stats,
                }
            )

        # Return the count and the list of the enriched_campaigns
        return {
            "campaigns": enriched_campaigns,
            "count": len(enriched_campaigns),
        }

    @staticmethod
    def get_campaign_details(campaign_id: UUID) -> dict:
        # Find the campaign_stats from the incoming campaign_id
        campaign_stats = CampaignStatsService.get_campaign_stats(campaign_id)

        # Find the campaign from the incomgin campaign_id
        campaign = CampaignRepository.get_campaign_with_emails(campaign_id)

        # return the campaign_stats and campaign, the response will be changed at the serialzer level.
        return {
            "campaign": campaign,
            "stats": campaign_stats,
        }
