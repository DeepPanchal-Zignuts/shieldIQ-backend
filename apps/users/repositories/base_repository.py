# Generic repository providing standard database operations.
from typing import Optional, Type
from django.db import models
from uuid import UUID
from common.exceptions.custom_exceptions import NotFoundException
from common.constants.error_code import ErrorCodes


class BaseRepository:
    model: Type[models.Model] = None

    @classmethod
    def exists(cls, **kwargs) -> bool:
        # Check whether a record matching the filters exists.
        return cls.model.objects.filter(**kwargs).exists()

    @classmethod
    def get_by_field(
        cls, raise_exception: bool = True, **kwargs
    ) -> Optional[models.Model]:
        # Retrieve a single record matching the given field(s).
        try:
            return cls.model.objects.get(**kwargs)
        except cls.model.DoesNotExist:
            if raise_exception:
                raise NotFoundException(
                    message=f"{cls.model.__name__} not found.",
                    error_code=ErrorCodes.NOT_FOUND,
                )
            return None

    @classmethod
    def get_by_id(
        cls, record_id: UUID, raise_exception: bool = True
    ) -> Optional[models.Model]:
        """Retrieve a single record by primary key."""
        try:
            return cls.model.objects.get(pk=record_id, is_deleted=False)
        except cls.model.DoesNotExist:
            if raise_exception:
                raise NotFoundException(
                    message=f"{cls.model.__name__} with id '{record_id}' not found.",
                    error_code=ErrorCodes.NOT_FOUND,
                )
            return None
