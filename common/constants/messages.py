"""
Centralized response messages for the entire application.
Avoid hardcoding strings in controllers/services.

Usage:
    from common.messages.messages import AuthMessages
"""


class BaseMessages:
    INTERNAL_SERVER_ERROR = "An internal server error occurred."
    BAD_REQUEST = "Bad Request."
    NOT_FOUND = "The requested resource was not found."
    CONFLICT = "A conflict occurred with the current state of the resource."
    RATE_LIMIT_EXCEEDED = "Too many requests. Please try again later."
    SERVICE_UNAVAILABLE = "The service is temporarily unavailable."


class AuthMessages:
    # Registration
    REGISTER_SUCCESS = "Users registered successfully. Please verify your email."

    # Email Verification
    EMAIL_VERIFIED = "Email verified successfully"
    EMAIL_ALREADY_VERIFIED = "Email is already verified"
    EMAIL_NOT_VERIFIED = (
        "Your email is not verified. Please verify the email before login."
    )
    INVALID_VERIFICATION_TOKEN = "Invalid or expired verification link"
    INVALID_FORGOT_PASS_TOKEN = "Invalid or expired forgot password token link"

    # Reset Password
    RESET_PASSWORD_EMAIL_SENT = "Password reset email has been sent."
    SAME_PASSWORD_AS_CURRENT = "New password cannot be same as current password"
    PASSWORD_CHANGED_SUCCESSFULLY = "Password changed successfully."

    # Login
    LOGIN_SUCCESS = "Login successful"
    INVALID_CREDENTIALS = "Invalid email or password"
    ACCOUNT_NOT_VERIFIED = "Please verify your email before logging in"
    ACCOUNT_DEACTIVATED = "Your account has been deactivated."

    # Logout
    LOGOUT_SUCCESS = "Logged out successfully"

    # Token
    TOKEN_EXPIRED = "Token expired. Please login again"
    INVALID_TOKEN = "Invalid authentication token"


class UserMessages:
    USER_NOT_FOUND = "Users not found"
    USER_UPDATED = "Users updated successfully"
    USER_DELETED = "Users deleted successfully"
    USER_WITH_EMAIL_ALREADY_EXISTS = "A user with this email already exists."
    EMAIL_SENDING_FAILED = "Failed to send verification email to {}"
    USER_PROFILE_SUCCESS = "Users details Fetched Successfully."
    USERS_FETCH_SUCCESS = "Users fetched Successfully."


class PermissionMessages:
    PERMISSION_DENIED = "You do not have permission to perform this action"
    AUTH_CREDS_INVALID = "Authentication credentials were not provided or are invalid."
    INVALID_AUTHORIZATION_TOKEN = "Invalid authorization token."


class ValidationMessages:
    REQUIRED_FIELD = "{} is required"
    VALIDATION_FAILED = "Validation Failed."
    INVALID_EMAIL = "Invalid email format"
    PASSWORD_TOO_SHORT = "Password must be at least 8 characters long."
    PASSWORD_UPPER_CASE = "Password must contain at least one uppercase letter."
    PASSWORD_LOWER_CASE = "Password must contain at least one lowercase letter."
    PASSWORD_DIGIT = "Password must contain at least one digit."
    PASSWORD_SPECIAL_CHAR = "Password must contain at least one special character."
    PASSWORD_NOT_MATCH = "Passwords do not match"


class DepartmentMessages:
    INVALID_DEPARTMENT_ENUM = "Invalid department value"


class CampaignMessages:
    END_DATE_GREATER_THAN_START_DATE = "end_date must be greater than start_date"
    START_DATE_GREATER_THAN_TODAY = "start_date must be greater than or equal to today"
    CAMPAIGN_CREATED = "Campaigns created successfully"
    CAMPAIGN_NOT_FOUND = "Campaigns not found"
    CAMPAIGN_UPDATED = "Campaigns updated successfully"
    CAMPAIGN_DELETED = "Campaigns deleted successfully"
    CAMPAIGN_FETCHED = "Campaigns fetched successfully"
    CAMPAIGNS_FETCHED = "Campaigns fetched successfully"
    NO_CAMPAIGNS_FOUND = "No campaigns found"

    # Campaigns emails
    CAMPAIGN_EMAIL_CREATED = "Campaigns email created successfully"
    CAMPAIGN_EMAIL_NOT_FOUND = "Campaigns email not found"

    # Campaigns events
    CAMPAIGN_EVENT_CREATED = "Campaigns event created successfully"
    CAMPAIGN_EVENT_ALREADY_REGISTERED = "Campaigns event already registered."


class DashboardMeessages:
    DASHBOARD_DATA_FETCHED = "Dashboard data fetched successfully"
