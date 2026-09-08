import re

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


class ContactValidator(BaseEngine):
    """
    Validates citizen contact information.
    """

    MOBILE_PATTERN = re.compile(
        r"^[6-9]\d{9}$"
    )

    EMAIL_PATTERN = re.compile(
        r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    )

    def validate(
        self,
        db: Session,
        request: ComplaintRequest,
        result: ValidationResult,
    ) -> None:
        """
        Validate citizen contact information.
        """

        self.validate_mobile(
            request,
            result,
        )

        self.validate_email(
            request,
            result,
        )

    def validate_mobile(
        self,
        request: ComplaintRequest,
        result: ValidationResult,
    ) -> None:

        if request.mobile_number is None:
            return

        mobile = request.mobile_number.strip()

        if not mobile:
            return

        if not self.MOBILE_PATTERN.fullmatch(
            mobile
        ):
            result.add_error(
                field="mobile_number",
                error_code="INVALID_MOBILE",
                message="Invalid mobile number.",
            )

    def validate_email(
        self,
        request: ComplaintRequest,
        result: ValidationResult,
    ) -> None:

        if request.email is None:
            return

        email = request.email.strip()

        if not email:
            return

        if not self.EMAIL_PATTERN.fullmatch(
            email
        ):
            result.add_error(
                field="email",
                error_code="INVALID_EMAIL",
                message="Invalid email address.",
            )