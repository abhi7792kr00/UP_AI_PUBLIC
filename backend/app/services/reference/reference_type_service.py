from app.services.base.base_service import BaseService

from app.repositories.reference.reference_type_repository import (
    reference_type_repository,
)

from database.models.reference.reference_type import (
    ReferenceType,
)


class ReferenceTypeService(
    BaseService[ReferenceType]
):
    def __init__(self):
        super().__init__(
            repository=reference_type_repository
        )


reference_type_service = (
    ReferenceTypeService()
)