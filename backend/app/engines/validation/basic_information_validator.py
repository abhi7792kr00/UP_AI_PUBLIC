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


class BasicInformationValidator(BaseEngine):
    """
    Validates the basic complaint information.
    """

    SUBJECT_MIN_LENGTH = 5
    SUBJECT_MAX_LENGTH = 200

    DESCRIPTION_MIN_LENGTH = 20
    DESCRIPTION_MAX_LENGTH = 5000

    def validate(
        self,
        db: Session,
        request: ComplaintRequest,
        result: ValidationResult,
    ) -> None:
        """
        Validate complaint basic information.

        db is accepted to keep a common validator
        interface across the validation layer.
        """

        self.validate_subject(
            request,
            result,
        )

        self.validate_description(
            request,
            result,
        )

    def validate_subject(
        self,
        request: ComplaintRequest,
        result: ValidationResult,
    ) -> None:
        """
        Validate complaint subject.
        """

        subject = request.subject.strip()

        if not subject:
            result.add_error(
                field="subject",
                error_code="SUBJECT_REQUIRED",
                message="Complaint subject is required.",
            )
            return

        if len(subject) < self.SUBJECT_MIN_LENGTH:
            result.add_error(
                field="subject",
                error_code="SUBJECT_TOO_SHORT",
                message=(
                    f"Complaint subject must be at least "
                    f"{self.SUBJECT_MIN_LENGTH} characters."
                ),
            )

        if len(subject) > self.SUBJECT_MAX_LENGTH:
            result.add_error(
                field="subject",
                error_code="SUBJECT_TOO_LONG",
                message=(
                    f"Complaint subject must not exceed "
                    f"{self.SUBJECT_MAX_LENGTH} characters."
                ),
            )

    def validate_description(
        self,
        request: ComplaintRequest,
        result: ValidationResult,
    ) -> None:
        """
        Validate complaint description.
        """

        description = request.description.strip()

        if not description:
            result.add_error(
                field="description",
                error_code="DESCRIPTION_REQUIRED",
                message="Complaint description is required.",
            )
            return

        if len(description) < self.DESCRIPTION_MIN_LENGTH:
            result.add_error(
                field="description",
                error_code="DESCRIPTION_TOO_SHORT",
                message=(
                    f"Complaint description must be at least "
                    f"{self.DESCRIPTION_MIN_LENGTH} characters."
                ),
            )

        if len(description) > self.DESCRIPTION_MAX_LENGTH:
            result.add_error(
                field="description",
                error_code="DESCRIPTION_TOO_LONG",
                message=(
                    f"Complaint description must not exceed "
                    f"{self.DESCRIPTION_MAX_LENGTH} characters."
                ),
            )