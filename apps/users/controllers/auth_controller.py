from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ViewSet
from apps.users.serializers.user_serializer import (
    ForgotPasswordSerializer,
    RegisterSerializer,
    LoginSerializer,
    ResetPasswordSerializer,
    VerifyEmailSerializer,
    RegisterResponseSerializer,
    LoginResponseSerializer,
)
from apps.users.services.auth_service import AuthService
from common.responses.api_response import ApiResponse
from common.constants.messages import AuthMessages


class AuthController(ViewSet):

    # POST /api/v1/auth/register
    @action(
        detail=False,
        methods=["post"],
        url_path="register",
        url_name="register",
        permission_classes=[AllowAny],
        authentication_classes=[],
    )
    def register_user(self, request):
        # Validate the input data
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Register the user
        user_data = AuthService.register(data=serializer.validated_data)

        # Serialize the response data
        response_data = RegisterResponseSerializer(
            {
                "user": user_data["user"],
            }
        )

        return ApiResponse.created(
            data=response_data.data,
            message=AuthMessages.REGISTER_SUCCESS,
        )

    # POST /api/v1/auth/login
    @action(
        detail=False,
        methods=["post"],
        url_path="login",
        url_name="login",
        permission_classes=[AllowAny],
        authentication_classes=[],
    )
    def login_user(self, request):
        # Validate the input data
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Login the user
        user_data = AuthService.login(
            email=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
        )

        # Serialize the response data
        response_data = LoginResponseSerializer(
            {
                "user": user_data["user"],
                "tokens": user_data["tokens"],
            }
        )

        return ApiResponse.success(
            data=response_data.data,
            message=AuthMessages.LOGIN_SUCCESS,
        )

    # POST /api/v1/auth/verify-email
    @action(
        detail=False,
        methods=["post"],
        url_path="verify-email",
        url_name="verify-email",
        permission_classes=[AllowAny],
        authentication_classes=[],
    )
    def verify_email(self, request):
        # Validate the input data
        serializer = VerifyEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Verify the email
        AuthService.verify_email(
            token=serializer.validated_data["verification_token"],
        )

        return ApiResponse.success(
            message=AuthMessages.EMAIL_VERIFIED,
        )

    # POST /api/v1/auth/forgot-password
    @action(
        detail=False,
        methods=["post"],
        url_path="forgot-password",
        url_name="forgot-password",
        permission_classes=[AllowAny],
        authentication_classes=[],
    )
    def forgot_password(self, request):
        # Validate the input data
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Send reset password email
        AuthService.forgot_password(
            email=serializer.validated_data["email"],
        )

        return ApiResponse.success(
            message=AuthMessages.RESET_PASSWORD_EMAIL_SENT,
        )

    # POST /api/v1/auth/reset-password
    @action(
        detail=False,
        methods=["post"],
        url_path="reset-password",
        url_name="reset-password",
        permission_classes=[AllowAny],
        authentication_classes=[],
    )
    def reset_password(self, request):
        # Validate the input data
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Reset the password
        AuthService.reset_password(
            forgot_password_token=serializer.validated_data["forgot_password_token"],
            password=serializer.validated_data["password"],
        )

        return ApiResponse.success(
            message=AuthMessages.PASSWORD_CHANGED_SUCCESSFULLY,
        )

    # POST /api/v1/auth/logout
    @action(
        detail=False,
        methods=["post"],
        url_path="logout",
        url_name="logout",
        permission_classes=[IsAuthenticated],
    )
    def logout(self, request):
        # Logout the user
        AuthService.logout(request.auth)

        return ApiResponse.success(
            message=AuthMessages.LOGOUT_SUCCESS,
        )
