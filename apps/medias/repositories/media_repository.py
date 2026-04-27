# apps/medias/repositories/media_repository.py

from apps.medias.models.media_model import Medias
from utils import date_utils


class MediaRepository:

    @staticmethod
    def create_media(data: dict) -> Medias:
        return Medias.objects.create(**data)

    @staticmethod
    def get_medias_by_user(user_id):
        return Medias.objects.filter(user_id=user_id, is_deleted=False)

    @staticmethod
    def get_media_by_id(media_id):
        return Medias.objects.filter(id=media_id).first()

    @staticmethod
    def delete_media(media):
        media.is_deleted = True
        media.deleted_at = date_utils.get_now()
        media.save()
