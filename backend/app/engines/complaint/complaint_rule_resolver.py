from sqlalchemy.orm import Session

from app.dto.complaint.complaint_request import (
    ComplaintRequest,
)

from app.dto.complaint.complaint_rule_result import (
    ComplaintRuleResult,
)

from app.engines.base.base_engine import (
    BaseEngine,
)


class ComplaintRuleResolver(BaseEngine):
    """
    Resolves complaint routing and business rules.
    """

    def __init__(
        self,
        complaint_category_mapping_service,
    ):
        self.complaint_category_mapping_service = (
            complaint_category_mapping_service
        )

    def resolve(
        self,
        db: Session,
        request: ComplaintRequest,
    ) -> ComplaintRuleResult:
        """
        Resolve complaint routing rule.
        """

        mapping = (
            self.complaint_category_mapping_service.get_by_category(
                db,
                request.category_id,
            )
        )

        if mapping is None:
            raise ValueError(
                "Complaint routing rule not configured."
            )

        return ComplaintRuleResult(
            administrative_level_id=(
                mapping.administrative_level_id
            ),
            department_id=mapping.department_id,
            office_id=mapping.office_id,
            designation_id=mapping.designation_id,
            priority_id=mapping.priority_id,
            sla_days=mapping.sla_days,
        )