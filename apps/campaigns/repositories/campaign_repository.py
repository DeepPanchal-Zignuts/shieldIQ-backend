from uuid import UUID

from django.db import connection
from django.db.models import Prefetch
from apps.campaigns.models.campaign_email_model import CampaignEmails
from apps.campaigns.models.campaign_model import Campaigns
from common.constants import constants
from common.constants.error_code import ErrorCodes
from common.constants.messages import CampaignMessages
from common.exceptions.custom_exceptions import NotFoundException
from utils import date_utils


class CampaignRepository:

    @classmethod
    def create_campaign(cls, data: dict) -> Campaigns:
        return Campaigns.objects.create(**data)

    @classmethod
    def get_campaign_by_id(
        cls,
        campaign_id: UUID,
    ) -> Campaigns:
        data = {
            "id": campaign_id,
            "is_deleted": False,
        }
        try:
            return Campaigns.objects.get(**data)
        except Campaigns.DoesNotExist as e:
            raise NotFoundException(
                message=str(e),
                error_code=ErrorCodes.NOT_FOUND,
            )

    @classmethod
    def get_campaigns_by_user_id(cls, user_id: UUID):
        return Campaigns.objects.filter(
            created_by=user_id,
            is_deleted=False,
        ).order_by("-created_at")

    @classmethod
    def get_campaign_with_emails(cls, campaign_id):
        campaign = (
            Campaigns.objects.filter(
                id=campaign_id,
                is_deleted=False,
            )
            .prefetch_related(
                Prefetch(
                    "emails",
                    queryset=CampaignEmails.objects.filter(is_deleted=False).order_by(
                        "created_at"
                    ),
                )
            )
            .first()
        )

        if not campaign:
            raise NotFoundException(
                message=CampaignMessages.CAMPAIGN_NOT_FOUND,
                error_code=ErrorCodes.NOT_FOUND,
            )

        return campaign

    @classmethod
    def update_campaign(cls, campaign_id: UUID, data: dict) -> Campaigns:
        # Find the campaign to update
        campaign = CampaignRepository.get_campaign_by_id(campaign_id)

        # Update the campaign fields
        for field, value in data.items():
            setattr(campaign, field, value)

        # Save the campaign
        campaign.save()

        return campaign

    @classmethod
    def delete_campaign(cls, campaign_id: UUID) -> None:
        # Find the campaign to delete
        campaign = CampaignRepository.get_campaign_by_id(campaign_id)

        # set the is_deleted flag to True for soft deletion and update the deleted_at time to current time.
        campaign.is_deleted = True
        campaign.deleted_at = date_utils.get_now()

        # Save the campaign
        campaign.save()

    @classmethod
    def get_user_campaign_emails(cls, user_id: UUID, filters: dict) -> dict:
        search = filters.get("search")
        page = max(1, filters.get("page", 1))
        page_size = max(1, min(filters.get("page_size", 10), 100))  # Cap at 100
        ordering = filters.get("ordering", "-created_at")

        offset = (page - 1) * page_size

        # Sorting
        order_by = "CE.CREATED_AT DESC"
        if ordering:
            field = ordering.lstrip("-")
            direction = "DESC" if ordering.startswith("-") else "ASC"

            allowed_fields = ["created_at"]
            if field in allowed_fields:
                order_by = f"CE.{field.upper()} {direction}"

        # Search
        search_query = ""
        params = [str(user_id)]

        if search:
            search_query = """
                AND (
                    CE.SUBJECT ILIKE %s OR
                    CE.BODY ILIKE %s OR
                    CE.SENDER ILIKE %s
                )
            """
            search_term = f"%{search}%"
            params.extend([search_term, search_term, search_term])

        # 🔹 Count Query
        count_sql = f"""
            SELECT COUNT(CE.ID)
            FROM CAMPAIGNS C
            LEFT JOIN CAMPAIGN_EMAILS CE ON CE.CAMPAIGN_ID = C.ID
            LEFT JOIN USERS U ON C.TARGET_DEPARTMENTS ? U.DEPARTMENT
            WHERE
                U.ID = %s
                AND U.IS_DELETED = FALSE
                AND C.IS_DELETED = FALSE
                AND C.STATUS = '{constants.CampaignStatusEnum.ACTIVE}'
                {search_query}
        """

        # 🔹 Data Query
        data_sql = f"""
            SELECT CE.*,
            EXISTS (
                SELECT 1
                FROM CAMPAIGN_EVENTS CEV
                WHERE 
                    CEV.CAMPAIGN_EMAIL_ID = CE.ID
                    AND CEV.USER_ID = %s
                    AND CEV.IS_DELETED = FALSE
            ) AS is_user_interacted
            FROM CAMPAIGNS C
            LEFT JOIN CAMPAIGN_EMAILS CE ON CE.CAMPAIGN_ID = C.ID
            LEFT JOIN USERS U ON C.TARGET_DEPARTMENTS ? U.DEPARTMENT
            WHERE
                U.ID = %s
                AND U.IS_DELETED = FALSE
                AND C.IS_DELETED = FALSE
                AND C.STATUS = '{constants.CampaignStatusEnum.ACTIVE}'
                {search_query}
            ORDER BY {order_by}
            LIMIT %s OFFSET %s
        """

        with connection.cursor() as cursor:
            # Count
            cursor.execute(count_sql, params)
            total_count = cursor.fetchone()[0]

            # Data
            cursor.execute(data_sql, [str(user_id)] + params + [page_size, offset])
            columns = [col.name for col in cursor.description]
            rows = cursor.fetchall()

        results = [dict(zip(columns, row)) for row in rows]

        return {
            "count": total_count,
            "results": results,
        }
