from sqlalchemy.orm import Session

from app.repositories.complaint import (
    complaint_category_mapping_repository,
)

from app.services.base.base_service import (
    BaseService,
)


class ComplaintCategoryMappingService(
    BaseService
):
    """
    Service for Complaint Category Mapping.
    """

    def __init__(self):
        super().__init__(
            complaint_category_mapping_repository,
        )

    def get_by_category(
        self,
        db: Session,
        category_id: int,
    ):
        return (
            self.repository.get_by_category(
                db,
                category_id,
            )
        )


complaint_category_mapping_service = (
    ComplaintCategoryMappingService()
)