from typing import Optional
from uuid import UUID
from apps.users.models.user_model import User
from apps.users.repositories.base_repository import BaseRepository
from utils import date_utils


class UserRepository(BaseRepository):
    model = User

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
    def get_by_email(cls, email: str, raise_exception: bool = True) -> Optional[User]:
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
    ) -> Optional[User]:
        return cls.get_by_field(
            **{
                token_field: token,
                "is_deleted": False,
            },
            raise_exception=raise_exception,
        )
