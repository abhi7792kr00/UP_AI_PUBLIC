from app.services.base.base_service import BaseService

from app.repositories.reference.reference_sequence_repository import (
    reference_sequence_repository,
)

from database.models.reference.reference_sequence import (
    ReferenceSequence,
)


class ReferenceSequenceService(
    BaseService[ReferenceSequence]
):
    def __init__(self):
        super().__init__(
            repository=reference_sequence_repository
        )


reference_sequence_service = (
    ReferenceSequenceService()
)