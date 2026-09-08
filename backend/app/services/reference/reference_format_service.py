from app.services.base.base_service import BaseService

from app.repositories.reference.reference_format_repository import (
    reference_format_repository,
)

from database.models.reference.reference_format import (
    ReferenceFormat,
)


class ReferenceFormatService(
    BaseService[ReferenceFormat]
):
    def __init__(self):
        super().__init__(
            repository=reference_format_repository
        )


reference_format_service = (
    ReferenceFormatService()
)