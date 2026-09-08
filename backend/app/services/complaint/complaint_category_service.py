from sqlalchemy.orm import Session

from app.repositories.complaint import (
    complaint_category_repository,
)

from app.services.base.base_service import BaseService


class ComplaintCategoryService(
    BaseService
):
    """
    Service for Complaint Category.
    """

    def __init__(self):
        super().__init__(
            complaint_category_repository
        )

    # -----------------------
    # Query Methods
    # -----------------------

    def get_by_code(
        self,
        db: Session,
        category_code: str,
    ):
        return self.repository.get_by_code(
            db,
            category_code,
        )

    def get_by_name(
        self,
        db: Session,
        category_name: str,
    ):
        return self.repository.get_by_name(
            db,
            category_name,
        )


complaint_category_service = ComplaintCategoryService()