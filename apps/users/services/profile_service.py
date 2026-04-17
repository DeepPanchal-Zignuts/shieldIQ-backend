import uuid
from apps.users.repositories.user_repository import UserRepository
from common.exceptions.custom_exceptions import (
    BadRequestException,
)
from common.constants.messages import UserMessages
from common.constants.error_code import ErrorCodes


class ProfileService:

    @staticmethod
    def get_profile_details(user_id: uuid.UUID) -> dict:
        # Check if the user with the user_id exists in the database.
        user = UserRepository.get_by_id(user_id)
        if not user:
            raise BadRequestException(
                message=UserMessages.USER_NOT_FOUND,
                error_code=ErrorCodes.NOT_FOUND,
            )

        # Return the user object
        return {
            "user": user,
        }
