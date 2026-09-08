from pydantic import BaseModel, ConfigDict


class BaseDTO(BaseModel):
    """
    Base Data Transfer Object.

    All DTOs in the UP AI platform should inherit from this class.
    """

    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid",
        populate_by_name=True,
        validate_assignment=True,
    )