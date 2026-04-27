import json
from typing import Optional, Dict, Any
from uuid import UUID

from django.db import connection
from django.db.models import Q, QuerySet
from apps.users.models.user_model import Users
from apps.users.repositories.base_repository import BaseRepository
from common.constants import constants
from utils import date_utils


class UserRepository(BaseRepository):
    model = Users

    @classmethod
    def email_exists(cls, email: str) -> bool:
        # Check if a user with the given email already exists.
        return cls.exists(email=email.lower(), is_deleted=False)

    @classmethod
    def create_user(cls, **data):
        return cls.model.objects.create_user(**data)

    @classmethod
    def update_fields(cls, user, **fields):
        for key, value in fields.items():
            setattr(user, key, value)

        user.save(update_fields=list[str](fields.keys()))
        return user

    @classmethod
    def get_by_email(cls, email: str, raise_exception: bool = True) -> Optional[Users]:
        # Check if a user with the given email already exists.
        return cls.get_by_field(
            email=email.lower(), raise_exception=raise_exception, is_deleted=False
        )

    @classmethod
    def update_last_login(cls, user_id: UUID) -> None:
        """Update the last_login_at timestamp."""
        cls.model.objects.filter(pk=user_id, is_deleted=False).update(
            last_login_at=date_utils.get_now()
        )

    @classmethod
    def get_by_token(
        cls,
        token: str,
        token_field: str = "verification_token",
        raise_exception: bool = True,
    ) -> Optional[Users]:
        return cls.get_by_field(
            **{
                token_field: token,
                "is_deleted": False,
            },
            raise_exception=raise_exception,
        )

    @classmethod
    def get_all_users(
        cls,
        filters: Dict[str, Any] = None,
    ) -> QuerySet[Users]:
        # Define the filters to be applied to the queryset.
        filters = filters or {}

        # Create a queryset to fetch all the records from the db.
        queryset = cls.model.objects.all()

        # Apply the is_deleted=false filter by default.
        queryset = queryset.filter(is_deleted=False, is_staff=False)

        # Search based on the incoming filter.
        search = filters.get("search")
        if search:
            queryset = queryset.filter(
                Q(email__icontains=search) | Q(full_name__icontains=search)
            )

        # Apply additional filters if provided.
        if filters.get("is_active") is not None:
            queryset = queryset.filter(is_active=filters["is_active"])

        if filters.get("is_email_verified") is not None:
            queryset = queryset.filter(is_email_verified=filters["is_email_verified"])

        return queryset.order_by("-created_at")

    @classmethod
    def get_user_with_stats(cls, user_id: UUID) -> Optional[Dict]:
        """Fetch a single user's profile together with their engagement stats
        (average_score, click_rate, report_rate) in one raw SQL query."""
        sql = """
            SELECT
                u.id,
                u.email,
                u.full_name,
                u.department,
                u.security_score,
                u.is_active,
                u.is_staff,
                u.is_superuser,
                u.is_email_verified,
                u.created_at,
                u.updated_at,
                u.last_login_at,
                u.security_score::FLOAT AS average_score,
                COUNT(DISTINCT
                    CASE WHEN ce.is_phishing = TRUE THEN ev.campaign_email_id END
                ) AS phishing_emails_total,
                CASE
                    WHEN COUNT(DISTINCT
                             CASE WHEN ce.is_phishing = TRUE
                                  THEN ev.campaign_email_id END
                         ) = 0
                    THEN 0.0
                    ELSE
                        COUNT(DISTINCT
                            CASE WHEN ev.event_type = 'link_clicked'
                                      AND ce.is_phishing = TRUE
                                 THEN ev.campaign_email_id END
                        )::FLOAT
                        /
                        COUNT(DISTINCT
                            CASE WHEN ce.is_phishing = TRUE
                                 THEN ev.campaign_email_id END
                        )::FLOAT
                        * 100.0
                END AS click_rate,
                CASE
                    WHEN COUNT(DISTINCT
                             CASE WHEN ce.is_phishing = TRUE
                                  THEN ev.campaign_email_id END
                         ) = 0
                    THEN 0.0
                    ELSE
                        COUNT(DISTINCT
                            CASE WHEN ev.event_type = 'reported'
                                      AND ce.is_phishing = TRUE
                                 THEN ev.campaign_email_id END
                        )::FLOAT
                        /
                        COUNT(DISTINCT
                            CASE WHEN ce.is_phishing = TRUE
                                 THEN ev.campaign_email_id END
                        )::FLOAT
                        * 100.0
                END AS report_rate

            FROM users u
            LEFT JOIN campaign_events ev
                   ON ev.user_id       = u.id
                  AND ev.is_deleted    = FALSE
            LEFT JOIN campaign_emails ce
                   ON ce.id            = ev.campaign_email_id
                  AND ce.is_deleted    = FALSE
            WHERE u.id         = %s
              AND u.is_deleted = FALSE
            GROUP BY
                u.id,
                u.email,
                u.full_name,
                u.department,
                u.security_score,
                u.is_active,
                u.is_staff,
                u.is_superuser,
                u.is_email_verified,
                u.created_at,
                u.updated_at,
                u.last_login_at
        """

        with connection.cursor() as cursor:
            cursor.execute(sql, [str(user_id)])
            columns = [col.name for col in cursor.description]
            row = cursor.fetchone()

        if row is None:
            return None

        return dict(zip(columns, row))

    @classmethod
    def get_user_dashboard(cls, user_id: UUID) -> Optional[Dict]:
        """Fetch a single user's dashboard stats together with their recent activity messages."""
        sql = f"""
            SELECT
                U.ID,
                U.SECURITY_SCORE,
                COUNT(DISTINCT CE.ID) AS ATTACKS_FACED,
                COUNT(DISTINCT CEV.ID) FILTER (WHERE CEV.EVENT_TYPE = '{constants.CampaignEventsEnum.REPORTED}') AS REPORTED,
                COUNT(DISTINCT CEV.ID) FILTER (WHERE CEV.EVENT_TYPE = '{constants.CampaignEventsEnum.LINK_CLICKED}') AS CLICKED,
                COALESCE(
                    jsonb_agg(
                        DISTINCT jsonb_build_object(
                            'subject', CE2.SUBJECT,
                            'event_message',
                                CASE
                                    WHEN CEV2.EVENT_TYPE = '{constants.CampaignEventsEnum.OPENED}' THEN '{constants.CAMPAIGN_EVENT_MESSAGES[constants.CampaignEventsEnum.OPENED]}'
                                    WHEN CEV2.EVENT_TYPE = '{constants.CampaignEventsEnum.LINK_CLICKED}' THEN '{constants.CAMPAIGN_EVENT_MESSAGES[constants.CampaignEventsEnum.LINK_CLICKED]}'
                                    WHEN CEV2.EVENT_TYPE = '{constants.CampaignEventsEnum.REPORTED}' THEN '{constants.CAMPAIGN_EVENT_MESSAGES[constants.CampaignEventsEnum.REPORTED]}'
                                    ELSE CEV2.EVENT_TYPE
                                END,
                            'score_impact', CEV2.SCORE_IMPACT,
                            'created_at', CEV2.CREATED_AT
                        )
                    ) FILTER (WHERE CEV2.ID IS NOT NULL),
                    '[]'::jsonb
                ) AS events
            FROM USERS U
            LEFT JOIN CAMPAIGNS C 
                ON C.TARGET_DEPARTMENTS ? U.DEPARTMENT
                AND C.IS_DELETED = FALSE
                AND C.STATUS = '{constants.CampaignStatusEnum.ACTIVE}'
            LEFT JOIN CAMPAIGN_EMAILS CE 
                ON CE.CAMPAIGN_ID = C.ID
                AND CE.IS_DELETED = FALSE
            LEFT JOIN CAMPAIGN_EVENTS CEV 
                ON CEV.USER_ID = U.ID
                AND CEV.IS_DELETED = FALSE
            LEFT JOIN CAMPAIGN_EVENTS CEV2
                ON CEV2.USER_ID = U.ID
                AND CEV2.IS_DELETED = FALSE
            LEFT JOIN CAMPAIGN_EMAILS CE2
                ON CE2.ID = CEV2.CAMPAIGN_EMAIL_ID
                AND CE2.IS_DELETED = FALSE
            WHERE
                U.ID = %s
                AND U.DEPARTMENT IS NOT NULL
            GROUP BY
                U.ID;
        """

        with connection.cursor() as cursor:
            cursor.execute(sql, [str(user_id)])
            columns = [col.name for col in cursor.description]
            row = cursor.fetchone()

        if row is None:
            return None

        result = dict(zip(columns, row))

        if result.get("events") and isinstance(result["events"], str):
            result["events"] = json.loads(result["events"])

        return result

    @classmethod
    def update_security_score(cls, user_id: UUID, score: int) -> int:
        user = cls.model.objects.filter(id=user_id).first()
        if user is None:
            return 0  # or raise an exception
        new_score = max(0, min(100, user.security_score + score))
        user.security_score = new_score
        user.save(update_fields=["security_score"])

        return new_score

    @classmethod
    def delete_user(cls, user):
        user.is_deleted = True
        user.deleted_at = date_utils.get_now()
        user.is_active = False
        user.is_email_verified = False
        user.save(
            update_fields=["is_deleted", "deleted_at", "is_active", "is_email_verified"]
        )
