from common.constants import constants
from common.constants.error_code import ErrorCodes
from common.constants.messages import MediaMessages
from config import settings
from common.exceptions.custom_exceptions import ValidationException

from config.settings import SUPABASE_STORAGE_BUCKET
from core.supabase.client import supabase
import uuid
import logging

logger = logging.getLogger(__name__)


def upload_media(file, file_type, user):
    """Upload media to Supabase storage."""
    try:
        file_ext = file.name.split(".")[-1]
        file_name = f"{uuid.uuid4()}.{file_ext}"
        storage_path = f"{file_type}/{user.id}/{file_name}"
        file_bytes = file.read()

        supabase.storage.from_(SUPABASE_STORAGE_BUCKET).upload(
            path=storage_path,
            file=file_bytes,
            file_options={"content-type": file.content_type},
        )

        public_url = supabase.storage.from_(SUPABASE_STORAGE_BUCKET).get_public_url(
            storage_path
        )
        return {"url": public_url, "path": storage_path}
    except Exception as e:
        logger.exception(f"Error uploading media: {e}")
        return None


def validate_media(file, upload_type: str):
    # Check if upload type is valid
    if upload_type not in constants.UPLOAD_RULES:
        raise ValidationException(
            message=MediaMessages.INVALID_UPLOAD_TYPE,
            error_code=ErrorCodes.INVALID_UPLOAD_TYPE,
        )

    # Get rules for the upload type
    rules = constants.UPLOAD_RULES[upload_type]

    file_size = file.size
    if not file.content_type:
        raise ValidationException(
            message=MediaMessages.INVALID_UPLOAD_TYPE,
            error_code=ErrorCodes.INVALID_UPLOAD_TYPE,
        )
    file_type = file.content_type.split("/")[-1].lower()

    # Validate size
    if file_size > rules["max_size"]:
        raise ValidationException(
            message=MediaMessages.FILE_TOO_LARGE,
            error_code=ErrorCodes.FILE_SIZE_EXCEEDED,
        )

    # Validate type
    if file_type not in rules["allowed_types"]:
        raise ValidationException(
            message=MediaMessages.INVALID_UPLOAD_TYPE,
            error_code=ErrorCodes.INVALID_UPLOAD_TYPE,
        )


def delete_media(storage_path):
    """Delete media from Supabase storage."""
    try:
        supabase.storage.from_(settings.SUPABASE_STORAGE_BUCKET).remove([storage_path])
        return True
    except Exception as e:
        logger.exception(f"Error deleting media: {e}")
        return False
