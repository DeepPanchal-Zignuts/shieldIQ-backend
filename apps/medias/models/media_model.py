import uuid
from django.db import models


class Medias(models.Model):
    class Meta:
        db_table = "medias"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_index=True,
    )

    user = models.ForeignKey(
        "users.Users",
        on_delete=models.CASCADE,
        related_name="medias",
    )

    file_url = models.URLField()
    file_name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=50)
    file_size = models.IntegerField()
    bucket = models.CharField(max_length=100, null=True, blank=True)
    storage_path = models.CharField(max_length=255, null=True, blank=True)

    # Timestamps (Milliseconds)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        "users.Users",
        on_delete=models.SET_NULL,
        null=True,
        related_name="media_created",
    )

    # Soft-delete
    is_deleted = models.BooleanField(default=False, db_index=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.file_name
