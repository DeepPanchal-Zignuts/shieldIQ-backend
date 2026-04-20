import uuid
from django.db import models


# CampaignEmail model represents the emails associated with the campaign in the system
class CampaignEmail(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_index=True,
    )
    campaign = models.ForeignKey(
        "campaigns.Campaign",
        on_delete=models.CASCADE,
        related_name="emails",
    )
    # Email metadata
    sender = models.CharField(max_length=255)
    from_email = models.EmailField(max_length=255)

    # Content
    subject = models.CharField(max_length=255)
    body = models.TextField()

    # Optional phishing CTA
    link_text = models.CharField(max_length=255, null=True, blank=True)

    # Flag
    is_phishing = models.BooleanField(default=False)

    # Timestamps (Milliseconds)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Soft-delete
    is_deleted = models.BooleanField(default=False, db_index=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.subject} ({self.from_email})"
