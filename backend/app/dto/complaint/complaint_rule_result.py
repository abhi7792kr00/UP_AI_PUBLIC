from app.dto.common.base import BaseDTO


class ComplaintRuleResult(BaseDTO):
    """
    Result returned by Complaint Rule Resolver.
    """

    administrative_level_id: int

    department_id: int

    office_id: int

    designation_id: int

    priority_id: int

    sla_days: int