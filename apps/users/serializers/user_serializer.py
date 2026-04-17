from rest_framework import serializers
from common.constants import constants
from common.constants.messages import ValidationMessages

# ══════════════════════════════════════════════════════════════
# Request Serializers (input validation)
# ══════════════════════════════════════════════════════════════


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, min_length=8, write_only=True)
    confirm_password = serializers.CharField(
        required=True, min_length=8, write_only=True
    )
    full_name = serializers.CharField(required=False, max_length=255, default="")
    department = serializers.ChoiceField(
        choices=constants.DepartmentEnum.choices,
        required=False,
        allow_null=True,
    )
    security_score = serializers.IntegerField(default=0)

    def validate(self, attrs):
        # validate passwords
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {"confirm_password": ValidationMessages.PASSWORD_NOT_MATCH}
            )

        return attrs


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, min_length=8, write_only=True)


class VerifyEmailSerializer(serializers.Serializer):
    verification_token = serializers.CharField(required=True)


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class ResetPasswordSerializer(serializers.Serializer):
    forgot_password_token = serializers.CharField(required=True)
    password = serializers.CharField(required=True, min_length=8, write_only=True)


# ══════════════════════════════════════════════════════════════
# Response Serializers (output formatting)
# ══════════════════════════════════════════════════════════════


class UserResponseSerializer(serializers.Serializer):
    """Serializes user data for API responses."""

    id = serializers.UUIDField()
    email = serializers.EmailField()
    full_name = serializers.CharField()
    is_email_verified = serializers.BooleanField()
    is_active = serializers.BooleanField()
    is_staff = serializers.BooleanField()
    department = serializers.ChoiceField(
        choices=constants.DepartmentEnum.choices, allow_null=True
    )
    security_score = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
    last_login_at = serializers.DateTimeField()


class UserDetailedResponseSerializer(serializers.Serializer):
    """Serializes user data for API responses."""

    id = serializers.UUIDField()
    email = serializers.EmailField()
    full_name = serializers.CharField()
    is_email_verified = serializers.BooleanField()
    is_active = serializers.BooleanField()
    is_staff = serializers.BooleanField()
    is_superuser = serializers.BooleanField()
    department = serializers.ChoiceField(
        choices=constants.DepartmentEnum.choices, allow_null=True
    )
    security_score = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
    last_login_at = serializers.DateTimeField()


class AuthTokenResponseSerializer(serializers.Serializer):
    """Serializes token pair returned on login/register."""

    access_token = serializers.CharField()
    refresh_token = serializers.CharField()
    token_type = serializers.CharField(default="Bearer")


class RegisterResponseSerializer(serializers.Serializer):
    user = UserResponseSerializer()


class LoginResponseSerializer(serializers.Serializer):
    """Combined login response with user + tokens."""

    user = UserResponseSerializer()
    tokens = AuthTokenResponseSerializer()


class UserProfileDetailsResponseSerializer(serializers.Serializer):
    user = UserDetailedResponseSerializer()
