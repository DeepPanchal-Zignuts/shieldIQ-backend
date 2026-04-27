from uuid import UUID
from apps.users.repositories.user_repository import UserRepository
from common.exceptions.custom_exceptions import (
    BadRequestException,
)
from common.constants.messages import UserMessages
from common.constants.error_code import ErrorCodes


class UserService:

    @staticmethod
    def get_profile_details(user_id: UUID) -> dict:
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

    @staticmethod
    def get_user_details(user_id: UUID) -> dict:
        # Fetch the user's details from the database
        user_details = UserRepository.get_user_with_stats(user_id)
        if not user_details:
            raise BadRequestException(
                message=UserMessages.USER_NOT_FOUND,
                error_code=ErrorCodes.NOT_FOUND,
            )

        # Return the user object
        return user_details

    @staticmethod
    def get_user_stats(user_id: UUID) -> dict:
        # Fetch the user's stats from the database
        user_stats = UserRepository.get_user_dashboard(user_id)
        if not user_stats:
            raise BadRequestException(
                message=UserMessages.USER_NOT_FOUND,
                error_code=ErrorCodes.NOT_FOUND,
            )

        # Return the user_stats object
        return user_stats

    @staticmethod
    def update_user(user_id: UUID, data):
        # Check if the user with the user_id exists in the database.
        user = UserRepository.get_by_id(user_id)
        if not user:
            raise BadRequestException(
                message=UserMessages.USER_NOT_FOUND,
                error_code=ErrorCodes.NOT_FOUND,
            )

        # Update the user
        updated_user = UserRepository.update_fields(user, **data)

        # Return the updated user object
        return {
            "user": updated_user,
        }

    @staticmethod
    def delete_user(user_id: UUID):
        # Check if the user with the user_id exists in the database.
        user = UserRepository.get_by_id(user_id)
        if not user:
            raise BadRequestException(
                message=UserMessages.USER_NOT_FOUND,
                error_code=ErrorCodes.NOT_FOUND,
            )

        # Delete the user
        UserRepository.delete_user(user)
