from config import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from common.exceptions.custom_exceptions import InternalServerErrorException
from common.constants import messages, error_code


# send_verification_email sends email to the user.
def send_verification_email(user, token: str) -> None:
    verify_url = f"{settings.FRONTEND_URL}/verify-email?token={token}"
    subject = "Verify Your Email to Activate Your ShieldIQ Account"

    # Create the context to send in the templates
    context = {
        "name": user.full_name or "there",
        "verify_url": verify_url,
        "expiry_hours": int(
            settings.EMAIL_VERIFICATION_TOKEN_LIFETIME.total_seconds() // 3600
        ),
    }

    text_content = render_to_string("email/verify_email.txt", context)
    html_content = render_to_string("email/verify_email.html", context)
    try:
        # Send the email
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],
        )
        email.attach_alternative(html_content, "text/html")
        email.send()
    except Exception as e:
        raise InternalServerErrorException(
            message=messages.UserMessages.EMAIL_SENDING_FAILED.format(user.email),
            error_code=error_code.ErrorCodes.INTERNAL_SERVER_ERROR,
            details={"error": str(e)},
        )


# send_reset_pass_email sends email to the user.
def send_reset_pass_email(user, token: str) -> None:
    reset_url = f"{settings.FRONTEND_URL}/reset-password?key={token}"
    subject = "Reset Your ShieldIQ Password"

    # Create the context to send in the templates
    context = {
        "name": user.full_name or "there",
        "reset_url": reset_url,
    }

    text_content = render_to_string("email/reset_password.txt", context)
    html_content = render_to_string("email/reset_password.html", context)
    try:
        # Send the email
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],
        )
        email.attach_alternative(html_content, "text/html")
        email.send()
    except Exception as e:
        raise InternalServerErrorException(
            message=messages.UserMessages.EMAIL_SENDING_FAILED.format(user.email),
            error_code=error_code.ErrorCodes.INTERNAL_SERVER_ERROR,
            details={"error": str(e)},
        )
