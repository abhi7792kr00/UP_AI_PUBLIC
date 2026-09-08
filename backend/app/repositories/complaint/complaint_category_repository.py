from sqlalchemy.orm import Session

from app.repositories.base.base_repository import BaseRepository

from database.models.complaint.complaint_category import (
    ComplaintCategory,
)


class ComplaintCategoryRepository(
    BaseRepository[ComplaintCategory]
):
    """
    Repository for Complaint Category.
    """

    def __init__(self):
        super().__init__(
            ComplaintCategory
        )

    # -----------------------
    # Query Methods
    # -----------------------

    def get_by_code(
        self,
        db: Session,
        category_code: str,
    ):
        return (
            db.query(ComplaintCategory)
            .filter(
                ComplaintCategory.category_code == category_code
            )
            .first()
        )

    def get_by_name(
        self,
        db: Session,
        category_name: str,
    ):
        return (
            db.query(ComplaintCategory)
            .filter(
                ComplaintCategory.category_name == category_name
            )
            .first()
        )


complaint_category_repository = ComplaintCategoryRepository()