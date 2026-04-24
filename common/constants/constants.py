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
    """Campaigns emails enum."""

    URGENT = "urgent", "Urgent"
    INVOICE = "invoice", "Invoice"
    PASSWORD_RESET = "password_reset", "Password Reset"
    GENERAL = "general", "General"


class CampaignStatusEnum(models.TextChoices):
    """Campaigns Status enum."""

    DRAFT = "draft", "Draft"
    ACTIVE = "active", "Active"
    COMPLETED = "completed", "Completed"


class CampaignEventsEnum(models.TextChoices):
    """Campaigns Events enum."""

    SENT = "sent", "Sent"
    OPENED = "opened", "Opened"
    LINK_CLICKED = "link_clicked", "Link Clicked"
    REPORTED = "reported", "Reported"


# Event Messages Mapping
CAMPAIGN_EVENT_MESSAGES = {
    CampaignEventsEnum.OPENED: "You opened an email",
    CampaignEventsEnum.LINK_CLICKED: "You clicked a malicious link",
    CampaignEventsEnum.REPORTED: "You reported a phishing email",
}
