from apps.campaigns.repositories.campaign_email_repository import (
    CampaignEmailRepository,
)
from apps.campaigns.repositories.campaign_repository import CampaignRepository
from apps.events.repositories.campaign_event_repository import CampaignEventRepository
from common.constants.error_code import ErrorCodes
from common.constants.messages import CampaignMessages
from common.exceptions.custom_exceptions import BadRequestException


class CampaignEventService:

    @staticmethod
    def create_campaign_event(campaign_id, campaign_email_id, user, event_type) -> dict:
        # Validate campaign
        campaign = CampaignRepository.get_campaign_by_id(campaign_id)
        if not campaign:
            raise BadRequestException(
                message=CampaignMessages.CAMPAIGN_NOT_FOUND,
                error_code=ErrorCodes.BAD_REQUEST,
            )

        # Validate campaign_email belongs to campaign
        campaign_email = CampaignEmailRepository.get_by_id_and_campaign(
            campaign_email_id, campaign.id
        )
        if not campaign_email:
            raise BadRequestException(
                message=CampaignMessages.CAMPAIGN_EMAIL_NOT_FOUND,
                error_code=ErrorCodes.BAD_REQUEST,
            )

        #  Prevent duplicate events
        if CampaignEventRepository.event_exists(
            campaign_email=campaign_email,
            user=user,
            event_type=event_type,
        ):
            raise BadRequestException(
                message=CampaignMessages.CAMPAIGN_EVENT_ALREADY_REGISTERED,
                error_code=ErrorCodes.BAD_REQUEST,
            )

        event = CampaignEventRepository.create_campaign_event(
            {
                "campaign": campaign,
                "campaign_email": campaign_email,
                "user": user,
                "event_type": event_type,
            }
        )

        return {"event": event}
