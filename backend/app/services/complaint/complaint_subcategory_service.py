from sqlalchemy.orm import Session

from app.repositories.complaint import (
    complaint_subcategory_repository,
)

from app.services.base.base_service import BaseService


class ComplaintSubCategoryService(
    BaseService
):
    def __init__(self):
        super().__init__(
            complaint_subcategory_repository
        )

    def get_by_category(
        self,
        db: Session,
        category_id: int,
    ):
        return self.repository.get_by_category(
            db,
            category_id,
        )

    def get_by_code(
        self,
        db: Session,
        code: str,
    ):
        return self.repository.get_by_code(
            db,
            code,
        )


complaint_subcategory_service = (
    ComplaintSubCategoryService()
)