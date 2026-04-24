from apps.users.models.user_model import Users
from apps.users.repositories.user_repository import UserRepository
from common.constants import constants


class ScoreEngine:

    @staticmethod
    def compute_score_impact(event_type: str, is_phishing: bool) -> int:
        """
        Returns the score delta for a given interaction.

        LINK_CLICKED + phishing     → -15
        REPORTED     + phishing     → +10
        LINK_CLICKED + safe email   →   0  (no penalty for clicking safe links)
        REPORTED     + safe email   →   0  (false positive — no change)
        SENT / OPENED               →   0  (passive events, no score impact)
        """
        if event_type == constants.CampaignEventsEnum.LINK_CLICKED:
            if is_phishing:
                return constants.PHISHING_CLICK_PENALTY
            return 0

        if event_type == constants.CampaignEventsEnum.REPORTED:
            if is_phishing:
                return constants.PHISHING_REPORT_REWARD
            return constants.FALSE_POSITIVE_PENALTY

        return 0

    @staticmethod
    def apply_score_delta(user_id, score: int) -> int:
        """
        Applies delta to user.security_score.
        Clamps between 0 and 100. Returns new score.
        """
        if score == 0:
            return Users.objects.get(id=user_id).security_score

        return UserRepository.update_security_score(user_id, score)
