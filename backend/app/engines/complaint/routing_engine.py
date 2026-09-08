from sqlalchemy.orm import Session

from app.engines.base.base_engine import (
    BaseEngine,
)

from app.dto.complaint.complaint_request import (
    ComplaintRequest,
)

from app.dto.complaint.routing_result import (
    RoutingResult,
)

from app.engines.complaint.officer_resolver import (
    officer_resolver,
)


class RoutingEngine(BaseEngine):
    """
    Resolves every routing component
    required before complaint creation.
    """

    def __init__(
        self,
        complaint_rule_resolver,
        workflow_resolver,
        status_resolver,
    ):
        self.complaint_rule_resolver = (
            complaint_rule_resolver
        )

        self.workflow_resolver = (
            workflow_resolver
        )

        self.status_resolver = (
            status_resolver
        )

    def resolve(
        self,
        db: Session,
        request: ComplaintRequest,
    ) -> RoutingResult:
        """
        Resolve complete routing.
        """

        rule = (
            self.complaint_rule_resolver.resolve(
                db,
                request,
            )
        )

        officer = (
            officer_resolver.resolve(
                db=db,
                department_id=rule.department_id,
                designation_id=rule.designation_id,
                office_id=rule.office_id,
            )
        )

        workflow, workflow_step = (
            self.workflow_resolver.resolve(
                db,
                module_name="COMPLAINT",
            )
        )

        status = (
            self.status_resolver.resolve(
                db,
            )
        )

        return RoutingResult(
            department_id=rule.department_id,

            office_id=rule.office_id,

            designation_id=rule.designation_id,

            officer_id=officer.id,

            priority_id=rule.priority_id,

            workflow_definition_id=workflow.id,

            workflow_step_id=workflow_step.id,

            status_id=status.id,
        )