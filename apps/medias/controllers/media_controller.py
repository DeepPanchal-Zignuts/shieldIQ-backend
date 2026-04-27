from rest_framework.viewsets import ViewSet
from rest_framework.parsers import MultiPartParser, FormParser
from apps.medias.serializers.media_serializer import MediaResponseSerializer
from apps.medias.services.media_service import MediaService
from common.constants.messages import MediaMessages
from common.responses.api_response import ApiResponse


class MediaController(ViewSet):
    parser_classes = [MultiPartParser, FormParser]

    # POST /api/v1/medias/upload-single
    def upload_single_media(self, request):
        file = request.FILES.get("file")
        file_type = request.data.get("file_type")
        upload_type = request.data.get("upload_type")

        if not file or not upload_type:
            return ApiResponse.error(
                message=MediaMessages.MISSING_MEDIA_OR_UPLOAD_TYPE,
            )

        file_obj = MediaService.upload_media(
            file=file,
            file_type=file_type,
            upload_type=upload_type,
            user=request.user,
        )

        response_data = MediaResponseSerializer(file_obj)

        return ApiResponse.created(
            data=response_data.data,
            message=MediaMessages.MEDIA_UPLOADED,
        )

    # DELETE /api/v1/medias/{media_id}
    def delete_single_media(self, request, pk=None):
        MediaService.delete_media(media_id=pk, user=request.user)

        return ApiResponse.success(message=MediaMessages.MEDIA_DELETED)
