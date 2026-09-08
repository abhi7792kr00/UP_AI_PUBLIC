from typing import Optional

from app.dto.common.base import BaseDTO


class StateDTO(BaseDTO):
    """
    Internal State Data Transfer Object.

    Used between the Service, Workflow,
    Engine, and Repository layers.
    """

    id: Optional[int] = None

    state_name: str

    state_code: str

    is_active: bool = True