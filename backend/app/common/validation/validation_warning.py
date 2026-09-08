from dataclasses import dataclass


@dataclass(slots=True)
class ValidationWarning:
    """
    Represents a non-blocking validation warning.
    """

    field: str
    warning_code: str
    message: str