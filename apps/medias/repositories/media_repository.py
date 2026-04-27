# apps/medias/repositories/media_repository.py

from apps.medias.models.media_model import Medias


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
