from django.db import models


class DepartmentEnum(models.TextChoices):
    """Departments within the organization."""

    IT_SECURITY = "it_security", "IT Security"
    ENGINEERING = "engineering", "Engineering"
    MARKETING = "marketing", "Marketing"
    HUMAN_RESOURCES = "human_resources", "Human Resources"
    FINANCE = "finance", "Finance"
    EXECUTIVE = "executive", "Executive"
