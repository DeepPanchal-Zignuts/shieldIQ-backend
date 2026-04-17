import uuid
from apps.users.repositories.user_repository import UserRepository
from common.exceptions.custom_exceptions import (
    BadRequestException,
)
from common.constants.messages import UserMessages
from common.constants.error_code import ErrorCodes


class UserService:

    @staticmethod
    def get_all_users(filters: dict) -> dict:
        # Fetch all the users from the database
        users = UserRepository.get_all_users(filters=filters)
        if len(users) == 0:
            raise BadRequestException(
                message=UserMessages.USER_NOT_FOUND,
                error_code=ErrorCodes.NOT_FOUND,
            )

        # Return the user object
        return {
            "users": users,
        }
