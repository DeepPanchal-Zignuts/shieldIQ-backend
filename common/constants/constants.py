from django.db import models


class DepartmentEnum(models.TextChoices):
    """Departments within the organization."""

    IT_SECURITY = "it_security", "IT Security"
    ENGINEERING = "engineering", "Engineering"
    MARKETING = "marketing", "Marketing"
    HUMAN_RESOURCES = "human_resources", "Human Resources"
    FINANCE = "finance", "Finance"
    EXECUTIVE = "executive", "Executive"


class CampaignEmailsEnum(models.TextChoices):
    """Campaign emails enum."""

    URGENT = "urgent", "Urgent"
    INVOICE = "invoice", "Invoice"
    PASSWORD_RESET = "password_reset", "Password Reset"
    GENERAL = "general", "General"


class CampaignStatusEnum(models.TextChoices):
    """Campaign Status enum."""

    DRAFT = "draft", "Draft"
    ACTIVE = "active", "Active"
    COMPLETED = "completed", "Completed"


class CampaignEventsEnum(models.TextChoices):
    """Campaign Events enum."""

    SENT = "sent", "Sent"
    OPENED = "opened", "Opened"
    LINK_CLICKED = "link_clicked", "Link Clicked"
    REPORTED = "reported", "Reported"
