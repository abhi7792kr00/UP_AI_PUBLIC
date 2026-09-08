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


class AttachmentValidator(BaseEngine):
    """
    Validates complaint attachments.

    Future validations:
    - File size
    - File extension
    - MIME type
    - Virus scan
    - Image compression
    """

    MAX_ATTACHMENTS = 10

    def validate(
        self,
        db: Session,
        request: ComplaintRequest,
        result: ValidationResult,
    ) -> None:
        """
        Validate attachment information.
        """

        if not request.has_attachment:
            return

        self.validate_attachment_metadata(
            request,
            result,
        )

    def validate_attachment_metadata(
        self,
        request: ComplaintRequest,
        result: ValidationResult,
    ) -> None:
        """
        Placeholder for future attachment validation.

        The current ComplaintRequest DTO only exposes
        a has_attachment flag. Detailed validation will
        be enabled after the attachment module is added.
        """

        return