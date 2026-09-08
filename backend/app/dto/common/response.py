from typing import Generic, Optional, TypeVar

from pydantic import Field

from app.dto.common.base import BaseDTO

T = TypeVar("T")


class ApiResponse(BaseDTO, Generic[T]):
    """
    Standard API Response DTO.
    """

    success: bool = True

    message: str = "Success"

    data: Optional[T] = Field(default=None)