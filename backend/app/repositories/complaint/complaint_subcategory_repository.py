from sqlalchemy.orm import Session

from app.repositories.base.base_repository import BaseRepository

from database.models.complaint.complaint_subcategory import (
    ComplaintSubCategory,
)


class ComplaintSubCategoryRepository(
    BaseRepository[ComplaintSubCategory]
):
    def __init__(self):
        super().__init__(ComplaintSubCategory)

    def get_by_category(
        self,
        db: Session,
        category_id: int,
    ):
        return (
            db.query(
                ComplaintSubCategory
            )
            .filter(
                ComplaintSubCategory.category_id == category_id
            )
            .all()
        )

    def get_by_code(
        self,
        db: Session,
        code: str,
    ):
        return (
            db.query(
                ComplaintSubCategory
            )
            .filter(
                ComplaintSubCategory.subcategory_code == code
            )
            .first()
        )


complaint_subcategory_repository = (
    ComplaintSubCategoryRepository()
)