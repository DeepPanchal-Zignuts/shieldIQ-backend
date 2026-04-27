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


class UserListRequestSerializer(serializers.Serializer):
    search = serializers.CharField(required=False, allow_blank=True, default=None)
    is_active = serializers.BooleanField(required=False, allow_null=True, default=None)
    is_email_verified = serializers.BooleanField(
        required=False, allow_null=True, default=None
    )


class UpdateUserRequestSerializer(serializers.Serializer):
    full_name = serializers.CharField(required=False, max_length=255)
    department = serializers.ChoiceField(
        choices=constants.DepartmentEnum.choices,
        required=False,
        allow_null=True,
    )
    profile_image_id = serializers.UUIDField(
        required=False,
        allow_null=True,
    )


# ══════════════════════════════════════════════════════════════
# Response Serializers (output formatting)
# ══════════════════════════════════════════════════════════════


class ProfileImageSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    file_url = serializers.CharField()


class UserResponseSerializer(serializers.Serializer):
    """Serializes user data for API responses."""

    id = serializers.UUIDField()
    email = serializers.EmailField()
    full_name = serializers.CharField()
    is_email_verified = serializers.BooleanField()
    is_active = serializers.BooleanField()
    department = serializers.ChoiceField(
        choices=constants.DepartmentEnum.choices, allow_null=True
    )
    security_score = serializers.IntegerField()
    profile_image = ProfileImageSerializer(required=False, allow_null=True)
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
    last_login_at = serializers.DateTimeField()


class AdminResponseSerializer(serializers.Serializer):
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
    profile_image = ProfileImageSerializer(required=False, allow_null=True)
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
    last_login_at = serializers.DateTimeField()


class AuthTokenResponseSerializer(serializers.Serializer):
    """Serializes token pair returned on login/register."""

    access_token = serializers.CharField()
    refresh_token = serializers.CharField()
    token_type = serializers.CharField(default="Bearer")


class RegisterResponseSerializer(serializers.Serializer):
    user = AdminResponseSerializer()


class LoginResponseSerializer(serializers.Serializer):
    """Combined login response with user + tokens."""

    user = AdminResponseSerializer()
    tokens = AuthTokenResponseSerializer()


class UserProfileDetailsResponseSerializer(serializers.Serializer):
    user = AdminResponseSerializer()


class StatsResponseSerializer(serializers.Serializer):
    average_score = serializers.FloatField()
    click_rate = serializers.FloatField()
    report_rate = serializers.FloatField()


class UserRecentActivityResponseSerializer(serializers.Serializer):
    subject = serializers.CharField()
    score_impact = serializers.IntegerField()
    event_message = serializers.CharField()
    created_at = serializers.DateTimeField()


class UserStatsDashboardResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    security_score = serializers.IntegerField()
    attacks_faced = serializers.IntegerField()
    reported = serializers.IntegerField()
    clicked = serializers.IntegerField()
    recent_activity = UserRecentActivityResponseSerializer(many=True, source="events")


class UserDetailsWithStatsResponseSerializer(serializers.Serializer):
    user = AdminResponseSerializer(source="*")
    stats = StatsResponseSerializer(source="*")


class UserListResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    email = serializers.EmailField()
    full_name = serializers.CharField()
    is_email_verified = serializers.BooleanField()
    is_active = serializers.BooleanField()
    department = serializers.ChoiceField(
        choices=constants.DepartmentEnum.choices, allow_null=True
    )
    security_score = serializers.IntegerField()
    profile_image = ProfileImageSerializer(required=False, allow_null=True)
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
    last_login_at = serializers.DateTimeField()
    average_score = serializers.FloatField()
    click_rate = serializers.FloatField()
    report_rate = serializers.FloatField()
