from sqlalchemy.orm import Session

from app.repositories.base.base_repository import (
    BaseRepository,
)

from database.models.complaint.complaint_category_mapping import (
    ComplaintCategoryMapping,
)


class ComplaintCategoryMappingRepository(
    BaseRepository[ComplaintCategoryMapping]
):
    """
    Repository for Complaint Category Mapping.
    """

    def __init__(self):
        super().__init__(
            ComplaintCategoryMapping,
        )

    def get_by_category(
        self,
        db: Session,
        category_id: int,
    ):
        return (
            db.query(
                ComplaintCategoryMapping,
            )
            .filter(
                ComplaintCategoryMapping.category_id
                == category_id,
            )
            .first()
        )


complaint_category_mapping_repository = (
    ComplaintCategoryMappingRepository()
)