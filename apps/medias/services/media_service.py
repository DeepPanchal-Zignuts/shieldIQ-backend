import logging
from django.db import transaction
from apps.medias.repositories.media_repository import MediaRepository
from common.constants.error_code import ErrorCodes
from common.constants.messages import MediaMessages
from common.exceptions.custom_exceptions import BadRequestException
from config import settings
from utils.media_upload import delete_media, upload_media, validate_media

logger = logging.getLogger(__name__)


class MediaService:

    @staticmethod
    def upload_media(file, file_type, upload_type, user):
        # Validate media
        validate_media(file, upload_type)

        # Call utility method to upload file to supabase
        file_url = upload_media(
            file,
            file_type,
            user,
        )
        if not file_url:
            raise BadRequestException(
                message=MediaMessages.MEDIA_UPLOAD_ERROR,
                error_code=ErrorCodes.MEDIA_UPLOAD_ERROR,
            )

        # Create media in the database
        try:
            with transaction.atomic():
                media = MediaRepository.create_media(
                    {
                        "user": user,
                        "file_url": file_url["url"],
                        "file_name": file.name,
                        "file_type": file.content_type,
                        "file_size": file.size,
                        "bucket": settings.SUPABASE_STORAGE_BUCKET,
                        "storage_path": file_url["path"],
                        "created_by": user,
                    }
                )
                return media
        except Exception as e:
            # Rollback external side-effect (Supabase cleanup)
            delete_media(file_url["path"])
            logger.exception(
                "Failed to create media record after Supabase upload: %s", e
            )
            raise BadRequestException(
                message=MediaMessages.MEDIA_UPLOAD_ERROR,
                error_code=ErrorCodes.MEDIA_UPLOAD_ERROR,
            )
