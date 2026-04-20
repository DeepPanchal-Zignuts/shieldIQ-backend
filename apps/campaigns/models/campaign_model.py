import uuid
from django.db import models
from common.constants import constants


# Campaign model represents the campaigns in the system
class Campaign(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_index=True,
    )
    title = models.CharField(
        max_length=155,
    )
    description = models.TextField(
        max_length=255,
    )
    start_date = models.DateField()
    end_date = models.DateField()
    target_departments = models.JSONField(default=list)
    email_type = models.CharField(
        max_length=50,
        choices=constants.CampaignEmailsEnum.choices,
    )
    status = models.CharField(
        max_length=50,
        default=constants.CampaignStatusEnum.DRAFT,
        choices=constants.CampaignStatusEnum.choices,
    )

    # Timestamps (Milliseconds)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="campaigns_created",
    )

    # Soft-delete
    is_deleted = models.BooleanField(default=False, db_index=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title
