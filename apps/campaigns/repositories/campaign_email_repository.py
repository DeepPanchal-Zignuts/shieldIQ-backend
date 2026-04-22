from uuid import UUID

from django.shortcuts import get_object_or_404
from apps.campaigns.models.campaign_email_model import CampaignEmails


class CampaignEmailRepository:

    @classmethod
    def create_campaign_email(cls, data: dict) -> CampaignEmails:
        return CampaignEmails.objects.create(**data)

    @staticmethod
    def get_by_id_and_campaign(campaign_email_id, campaign_id):
        return CampaignEmails.objects.filter(
            id=campaign_email_id,
            campaign_id=campaign_id,
            is_deleted=False,
        ).first()
