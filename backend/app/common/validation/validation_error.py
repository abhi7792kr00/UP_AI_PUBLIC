from dataclasses import dataclass


@dataclass(slots=True)
class ValidationError:
    """
    Represents a validation error.
    """

    field: str
    error_code: str
    message: str