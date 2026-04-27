from apps.campaigns.repositories.campaign_email_repository import (
    CampaignEmailRepository,
)
from apps.campaigns.repositories.campaign_repository import CampaignRepository
from apps.events.repositories.campaign_event_repository import CampaignEventRepository
from apps.events.services.score_engine import ScoreEngine
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
        ):
            raise BadRequestException(
                message=CampaignMessages.CAMPAIGN_EVENT_ALREADY_REGISTERED,
                error_code=ErrorCodes.BAD_REQUEST,
            )

        # Compute and apply score
        score = ScoreEngine.compute_score_impact(
            event_type=event_type,
            is_phishing=campaign_email.is_phishing,
        )

        event = CampaignEventRepository.create_campaign_event(
            {
                "campaign": campaign,
                "campaign_email": campaign_email,
                "user": user,
                "event_type": event_type,
                "score_impact": score,
            }
        )

        # Apply the score delta to the user's security score
        ScoreEngine.apply_score_delta(user_id=event.user_id, score=score)

        return {"event": event}
