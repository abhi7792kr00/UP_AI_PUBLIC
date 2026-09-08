from sqlalchemy.orm import Session

from app.common.validation.validation_result import (
    ValidationResult,
)

from app.dto.complaint.complaint_request import (
    ComplaintRequest,
)

from app.engines.base.base_engine import (
    BaseEngine,
)


class CategoryValidator(BaseEngine):
    """
    Validates complaint category
    and subcategory.
    """

    def __init__(
        self,
        category_repository,
        subcategory_repository,
    ):
        self.category_repository = (
            category_repository
        )

        self.subcategory_repository = (
            subcategory_repository
        )

    def validate(
        self,
        db: Session,
        request: ComplaintRequest,
        result: ValidationResult,
    ) -> None:
        """
        Validate category information.
        """

        category = self.validate_category(
            db,
            request,
            result,
        )

        self.validate_subcategory(
            db,
            request,
            result,
            category,
        )

    def validate_category(
        self,
        db: Session,
        request: ComplaintRequest,
        result: ValidationResult,
    ):
        """
        Validate complaint category.
        """

        category = (
            self.category_repository.get_by_id(
                db,
                request.category_id,
            )
        )

        if category is None:
            result.add_error(
                field="category_id",
                error_code="INVALID_CATEGORY",
                message="Complaint category does not exist.",
            )
            return None

        return category

    def validate_subcategory(
        self,
        db: Session,
        request: ComplaintRequest,
        result: ValidationResult,
        category,
    ) -> None:
        """
        Validate complaint subcategory.
        """

        if request.subcategory_id is None:
            return

        subcategory = (
            self.subcategory_repository.get_by_id(
                db,
                request.subcategory_id,
            )
        )

        if subcategory is None:
            result.add_error(
                field="subcategory_id",
                error_code="INVALID_SUBCATEGORY",
                message="Complaint subcategory does not exist.",
            )
            return

        if (
            category is not None
            and subcategory.category_id != category.id
        ):
            result.add_error(
                field="subcategory_id",
                error_code="CATEGORY_SUBCATEGORY_MISMATCH",
                message=(
                    "Selected subcategory does not belong "
                    "to the selected category."
                ),
            )