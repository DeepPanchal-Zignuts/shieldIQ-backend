from uuid import UUID

from django.shortcuts import get_object_or_404
from apps.campaigns.models.campaign_email_model import CampaignEmail


class CampaignEmailRepository:

    @classmethod
    def create_campaign_email(cls, data: dict) -> CampaignEmail:
        return CampaignEmail.objects.create(**data)

    @staticmethod
    def get_by_id_and_campaign(campaign_email_id, campaign_id):
        return CampaignEmail.objects.filter(
            id=campaign_email_id,
            campaign_id=campaign_id,
            is_deleted=False,
        ).first()
