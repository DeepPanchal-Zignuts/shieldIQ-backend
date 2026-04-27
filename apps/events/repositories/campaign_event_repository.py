from apps.events.models.campaign_events_model import CampaignEvents


class CampaignEventRepository:

    @classmethod
    def create_campaign_event(cls, data: dict) -> CampaignEvents:
        return CampaignEvents.objects.create(**data)

    @staticmethod
    def event_exists(campaign_email, user):
        return CampaignEvents.objects.filter(
            campaign_email=campaign_email,
            user=user,
            is_deleted=False,
        ).exists()
