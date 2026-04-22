import uuid
from django.db import models

from common.constants.constants import CampaignEventsEnum


# CampaignEvents model represents the events made on a campaign by a user
class CampaignEvents(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_index=True,
    )
    campaign = models.ForeignKey(
        "campaigns.Campaign",
        on_delete=models.CASCADE,
        related_name="events",
    )

    campaign_email = models.ForeignKey(
        "campaigns.CampaignEmail",
        on_delete=models.CASCADE,
        related_name="events",
    )

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="campaign_events",
    )

    event_type = models.CharField(
        max_length=20,
        choices=CampaignEventsEnum.choices,
    )
    score_impact = models.IntegerField(default=0)

    # Timestamps (Milliseconds)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Soft-delete
    is_deleted = models.BooleanField(default=False, db_index=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.event_type} - {self.campaign}"
