from dataclasses import dataclass, field

from app.common.validation.validation_error import ValidationError
from app.common.validation.validation_warning import ValidationWarning


@dataclass(slots=True)
class ValidationResult:
    """
    Result returned by all validators.
    """

    errors: list[ValidationError] = field(default_factory=list)

    warnings: list[ValidationWarning] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        return len(self.errors) == 0

    def add_error(
        self,
        field: str,
        error_code: str,
        message: str,
    ) -> None:
        self.errors.append(
            ValidationError(
                field=field,
                error_code=error_code,
                message=message,
            )
        )

    def add_warning(
        self,
        field: str,
        warning_code: str,
        message: str,
    ) -> None:
        self.warnings.append(
            ValidationWarning(
                field=field,
                warning_code=warning_code,
                message=message,
            )
        )