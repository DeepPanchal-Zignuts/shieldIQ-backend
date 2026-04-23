from typing import Optional, Dict, Any
from uuid import UUID

from django.db import connection
from django.db.models import Q, QuerySet
from apps.users.models.user_model import Users
from apps.users.repositories.base_repository import BaseRepository
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
