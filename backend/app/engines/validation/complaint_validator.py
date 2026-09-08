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

from app.engines.validation.basic_information_validator import (
    BasicInformationValidator,
)

from app.engines.validation.category_validator import (
    CategoryValidator,
)

from app.engines.validation.location_validator import (
    LocationValidator,
)

from app.engines.validation.contact_validator import (
    ContactValidator,
)

from app.engines.validation.attachment_validator import (
    AttachmentValidator,
)


class ComplaintValidator(BaseEngine):
    """
    Main orchestrator for complaint validation.

    Delegates validation to specialized validators.
    """

    def __init__(
        self,
        category_repository,
        subcategory_repository,
        state_repository,
        division_repository,
        district_repository,
        tehsil_repository,
        block_repository,
        gram_panchayat_repository,
        village_repository,
        municipal_body_repository,
        ward_repository,
        locality_repository,
    ):
        self.basic_information_validator = (
            BasicInformationValidator()
        )

        self.category_validator = (
            CategoryValidator(
                category_repository,
                subcategory_repository,
            )
        )

        self.location_validator = (
            LocationValidator(
                state_repository,
                division_repository,
                district_repository,
                tehsil_repository,
                block_repository,
                gram_panchayat_repository,
                village_repository,
                municipal_body_repository,
                ward_repository,
                locality_repository,
            )
        )

        self.contact_validator = (
            ContactValidator()
        )

        self.attachment_validator = (
            AttachmentValidator()
        )

    def validate(
        self,
        db: Session,
        request: ComplaintRequest,
    ) -> ValidationResult:
        """
        Validate complete complaint request.
        """

        result = ValidationResult()

        self.basic_information_validator.validate(
            db,
            request,
            result,
        )

        self.category_validator.validate(
            db,
            request,
            result,
        )

        self.location_validator.validate(
            db,
            request,
            result,
        )

        self.contact_validator.validate(
            db,
            request,
            result,
        )

        self.attachment_validator.validate(
            db,
            request,
            result,
        )

        return result