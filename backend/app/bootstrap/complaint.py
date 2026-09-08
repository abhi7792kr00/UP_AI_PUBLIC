"""
Complaint Bootstrap

Creates all complaint engines.
"""

from app.bootstrap.services import (
    complaint_service,
    complaint_priority_service,
    complaint_status_service,
    complaint_category_mapping_service,
)

from app.bootstrap.validators import (
    complaint_validator,
)

from app.bootstrap.workflow import (
    workflow_resolver,
    assignment_engine,
    timeline_engine,
)

from app.engines.complaint.priority_resolver import (
    PriorityResolver,
)

from app.engines.complaint.status_resolver import (
    StatusResolver,
)

from app.engines.complaint.complaint_rule_resolver import (
    ComplaintRuleResolver,
)

from app.engines.complaint.routing_engine import (
    RoutingEngine,
)

from app.engines.complaint.notification_engine import (
    NotificationEngine,
)

from app.engines.complaint.complaint_registration_engine import (
    ComplaintRegistrationEngine,
)

# ---------------------------------
# Resolvers
# ---------------------------------

priority_resolver = (
    PriorityResolver(
        complaint_priority_service,
    )
)

status_resolver = (
    StatusResolver(
        complaint_status_service,
    )
)

complaint_rule_resolver = (
    ComplaintRuleResolver(
        complaint_category_mapping_service,
    )
)

# ---------------------------------
# Engines
# ---------------------------------

routing_engine = (
    RoutingEngine(
        complaint_rule_resolver,
        workflow_resolver,
        status_resolver,
    )
)

notification_engine = (
    NotificationEngine()
)

complaint_registration_engine = (
    ComplaintRegistrationEngine(
        complaint_validator=complaint_validator,
        routing_engine=routing_engine,
        assignment_engine=assignment_engine,
        timeline_engine=timeline_engine,
        notification_engine=notification_engine,
        complaint_service=complaint_service,
    )
)

__all__ = [
    "priority_resolver",
    "status_resolver",
    "complaint_rule_resolver",
    "routing_engine",
    "notification_engine",
    "complaint_registration_engine",
]