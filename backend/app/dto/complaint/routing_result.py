from app.dto.common.base import BaseDTO


class RoutingResult(BaseDTO):
    """
    Complete routing information
    required for complaint registration.
    """

    department_id: int

    office_id: int

    designation_id: int

    officer_id: int

    priority_id: int

    workflow_definition_id: int

    workflow_step_id: int

    status_id: int