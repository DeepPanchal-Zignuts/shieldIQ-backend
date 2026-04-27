import uuid
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)
from django.db import models
from common.constants import constants
from common.constants.messages import ValidationMessages


#  UserManager creates users and superusers
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError(ValidationMessages.REQUIRED_FIELD.format("Email"))

        if not password:
            raise ValueError(ValidationMessages.REQUIRED_FIELD.format("Password"))

        email = self.normalize_email(email)
        kwargs.setdefault("is_active", True)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user


# Users model represents the users of the system
class Users(AbstractBaseUser, PermissionsMixin):

    class Meta:
        db_table = "users"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_index=True,
    )
    email = models.EmailField(
        unique=True,
        max_length=255,
        db_index=True,
    )
    full_name = models.CharField(
        max_length=255,
        blank=True,
    )
    department = models.CharField(
        max_length=50,
        choices=constants.DepartmentEnum.choices,
        null=True,
        blank=True,
    )
    security_score = models.IntegerField(
        default=0,
    )
    profile_image = models.ForeignKey(
        "medias.Medias",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="user_profile",
    )

    # JWT token
    access_token = models.TextField(null=True, blank=True)
    refresh_token = models.TextField(null=True, blank=True)
    verification_token = models.TextField(null=True, blank=True)
    forgot_password_token = models.TextField(null=True, blank=True)

    # Status flags
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)

    # Timestamps (Milliseconds)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login_at = models.DateTimeField(null=True, blank=True)
    forgot_password_at = models.DateTimeField(null=True, blank=True)

    # Soft-delete
    is_deleted = models.BooleanField(default=False, db_index=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []  # email is already required by USERNAME_FIELD

    def __str__(self):
        return self.email
