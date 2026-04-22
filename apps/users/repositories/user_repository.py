from typing import Optional, Dict, Any
from uuid import UUID

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
