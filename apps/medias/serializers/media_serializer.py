from rest_framework import serializers


# ══════════════════════════════════════════════════════════════
# Response Serializers (output formatting)
# ══════════════════════════════════════════════════════════════


class MediaResponseSerializer(serializers.Serializer):
    """Serializes media data for API responses."""

    id = serializers.UUIDField()
    file_url = serializers.URLField()
    file_name = serializers.CharField()
    file_type = serializers.CharField()
    file_size = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
    created_by = serializers.CharField()
