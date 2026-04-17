import uuid
from apps.users.repositories.user_repository import UserRepository
from common.validators.common_validators import (
    validate_email,
    validate_password_strength,
)
from common.exceptions.custom_exceptions import (
    ConflictException,
    UnauthorizedException,
    BadRequestException,
)
from config import settings
from utils import date_utils
from utils.encryption import hash_password, verify_password
from utils.token_utils import (
    generate_access_token,
    generate_refresh_token,
    verify_token,
)
from common.constants.messages import UserMessages, AuthMessages
from common.constants.error_code import ErrorCodes
from utils.send_mail import send_reset_pass_email, send_verification_email


class AuthService:

    @staticmethod
    def register(data: dict) -> dict:
        # Validate the email and password
        email = validate_email(data["email"])
        validate_password_strength(data["password"])

        # Check if the email already exists in the database
        if UserRepository.email_exists(email):
            raise ConflictException(
                message=UserMessages.USER_WITH_EMAIL_ALREADY_EXISTS,
                error_code=ErrorCodes.EMAIL_ALREADY_EXISTS,
            )

        # Hash the password and create the user
        user = UserRepository.create_user(
            email=email,
            full_name=data.get("full_name", ""),
            password=data["password"],
            department=data.get("department", ""),
            security_score=0,
        )

        # Generate email verification token and send email
        email_verification_token = generate_access_token(user)
        refresh_token = generate_refresh_token(user)

        # Update tokens in user
        UserRepository.update_fields(
            user,
            verification_token=email_verification_token,
            refresh_token=refresh_token,
        )

        # Send the verification email
        send_verification_email(user, email_verification_token)

        # Return the user object and the tokens
        return {
            "user": user,
        }

    @staticmethod
    def login(email: str, password: str) -> dict:
        # Validate the email and password
        email = validate_email(email)
        validate_password_strength(password)

        # Check if the user exists and the password is correct
        user = UserRepository.get_by_email(email, raise_exception=False)
        if not user:
            raise UnauthorizedException(
                message=AuthMessages.INVALID_CREDENTIALS,
                error_code=ErrorCodes.INVALID_CREDENTIALS,
            )

        # Verify the password
        if not verify_password(password, user.password):
            raise UnauthorizedException(
                message=AuthMessages.INVALID_CREDENTIALS,
                error_code=ErrorCodes.INVALID_CREDENTIALS,
            )

        # Check if the user's account is active
        if not user.is_active:
            raise UnauthorizedException(
                message=AuthMessages.ACCOUNT_DEACTIVATED,
                error_code=ErrorCodes.ACCOUNT_DEACTIVATED,
            )

        # Check if the user's email is verified
        if not user.is_email_verified:
            raise UnauthorizedException(
                message=AuthMessages.EMAIL_NOT_VERIFIED,
                error_code=ErrorCodes.EMAIL_NOT_VERIFIED,
            )

        # Update last login
        UserRepository.update_last_login(user.id)

        # Generate tokens for the user
        access_token = generate_access_token(user)
        refresh_token = generate_refresh_token(user)

        # Update tokens in user
        UserRepository.update_fields(
            user,
            access_token=access_token,
            refresh_token=refresh_token,
        )

        # Return the user object and the tokens
        return {
            "user": user,
            "tokens": {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "Bearer",
            },
        }

    @staticmethod
    def verify_email(token: str) -> dict:
        # Find the user with the incoming token.
        user = UserRepository.get_by_token(
            token, token_field="verification_token", raise_exception=True
        )
        if not user:
            raise BadRequestException(
                message=AuthMessages.INVALID_VERIFICATION_TOKEN,
                error_code=ErrorCodes.INVALID_TOKEN,
            )

        # Verify the token.
        token_data = verify_token(token, settings.ACCESS_SECRET_KEY)
        if not token_data["valid"]:
            raise BadRequestException(
                message=token_data["error"],
                error_code=ErrorCodes.INVALID_TOKEN,
            )

        # Update the user's email verification status.
        UserRepository.update_fields(
            user,
            verification_token=None,
            is_email_verified=True,
            is_active=True,
            updated_at=date_utils.get_now(),
        )

        return {
            "user": user,
        }

    @staticmethod
    def forgot_password(email: str) -> str:
        # Check if the user exists with the given email
        user = UserRepository.get_by_email(email, raise_exception=False)
        if not user:
            raise UnauthorizedException(
                message=UserMessages.USER_NOT_FOUND,
                error_code=ErrorCodes.NOT_FOUND,
            )

        # Check if the user's account is active
        if not user.is_active:
            raise UnauthorizedException(
                message=AuthMessages.ACCOUNT_DEACTIVATED,
                error_code=ErrorCodes.ACCOUNT_DEACTIVATED,
            )

        # Check if the user's email is verified
        if not user.is_email_verified:
            raise UnauthorizedException(
                message=AuthMessages.EMAIL_NOT_VERIFIED,
                error_code=ErrorCodes.EMAIL_NOT_VERIFIED,
            )

        # Generate a forget password token
        forgot_pass_token = str(uuid.uuid4())

        # Update the user's forgot password token
        UserRepository.update_fields(
            user,
            forgot_password_token=forgot_pass_token,
            forgot_password_at=date_utils.get_now(),
            updated_at=date_utils.get_now(),
        )

        # Send the reset password email
        send_reset_pass_email(user, forgot_pass_token)

        return {"user": user}

    @staticmethod
    def reset_password(forgot_password_token: str, password: str) -> str:
        # Find the user with the incoming token.
        user = UserRepository.get_by_token(
            forgot_password_token,
            token_field="forgot_password_token",
            raise_exception=True,
        )
        if not user:
            raise BadRequestException(
                message=AuthMessages.INVALID_FORGOT_PASS_TOKEN,
                error_code=ErrorCodes.INVALID_TOKEN,
            )

        # Check if token expired
        if (
            user.forgot_password_at + settings.FORGOT_PASSWORD_TOKEN_LIFETIME
            < date_utils.get_now()
        ):
            raise BadRequestException(
                message=AuthMessages.TOKEN_EXPIRED,
                error_code=ErrorCodes.TOKEN_EXPIRED,
            )

        # Check if new password == old password
        if verify_password(password, user.password):
            raise BadRequestException(
                message=AuthMessages.SAME_PASSWORD_AS_CURRENT,
                error_code=ErrorCodes.SAME_PASSWORD,
            )

        user.password = hash_password(password)
        user.forgot_password_token = None
        user.forgot_password_at = None
        user.access_token = None
        user.refresh_token = None
        user.updated_at = date_utils.get_now()
        user.save()

        return {"user": user}

    @staticmethod
    def logout(token: str) -> None:
        if token:
            user = UserRepository.get_by_token(token, token_field="access_token")

            if not user:
                raise BadRequestException(
                    message=UserMessages.USER_NOT_FOUND,
                    error_code=ErrorCodes.NOT_FOUND,
                )

            UserRepository.update_fields(
                user,
                access_token=None,
                refresh_token=None,
                updated_at=date_utils.get_now(),
            )

        return {"message": AuthMessages.LOGOUT_SUCCESS}
