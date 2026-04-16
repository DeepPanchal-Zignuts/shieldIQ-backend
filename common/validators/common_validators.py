import re
from common.exceptions.custom_exceptions import ValidationException
from common.constants import error_code, messages


# validate_email validates and return normalised email address
def validate_email(email: str) -> str:
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if not re.match(pattern, email):
        raise ValidationException(
            message=messages.ValidationMessages.INVALID_EMAIL,
            error_code=error_code.ErrorCodes.INVALID_EMAIL,
        )
    return email.lower().strip()


# validate_password_strength ensure password meets minimum strength requirements
def validate_password_strength(password: str) -> str:
    if len(password) < 8:
        raise ValidationException(
            message=messages.ValidationMessages.PASSWORD_TOO_SHORT,
            error_code=error_code.ErrorCodes.WEAK_PASSWORD,
        )
    if not re.search(r"[A-Z]", password):
        raise ValidationException(
            message=messages.ValidationMessages.PASSWORD_UPPER_CASE,
            error_code=error_code.ErrorCodes.WEAK_PASSWORD,
        )
    if not re.search(r"[a-z]", password):
        raise ValidationException(
            message=messages.ValidationMessages.PASSWORD_LOWER_CASE,
            error_code=error_code.ErrorCodes.WEAK_PASSWORD,
        )
    if not re.search(r"\d", password):
        raise ValidationException(
            message=messages.ValidationMessages.PASSWORD_DIGIT,
            error_code=error_code.ErrorCodes.WEAK_PASSWORD,
        )
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        raise ValidationException(
            message=messages.ValidationMessages.PASSWORD_SPECIAL_CHAR,
            error_code=error_code.ErrorCodes.WEAK_PASSWORD,
        )
    return password
