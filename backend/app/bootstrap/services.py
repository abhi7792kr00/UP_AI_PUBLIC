"""
Service Bootstrap

All services are exported from here.
"""

# ---------------------------------
# Auth
# ---------------------------------

from app.services.auth import (
    user_service,
)

# ---------------------------------
# Citizen
# ---------------------------------

from app.services.citizen import (
    citizen_service,
)

# ---------------------------------
# Complaint
# ---------------------------------

from app.services.complaint import (
    complaint_service,
    complaint_category_service,
    complaint_subcategory_service,
    complaint_priority_service,
    complaint_status_service,
    complaint_category_mapping_service,
)

# ---------------------------------
# Workflow
# ---------------------------------

from app.services.workflow import (
    workflow_definition_service,
    workflow_step_service,
    workflow_assignment_service,
    workflow_history_service,
)

__all__ = [

    # Auth
    "user_service",

    # Citizen
    "citizen_service",

    # Complaint
    "complaint_service",
    "complaint_category_service",
    "complaint_subcategory_service",
    "complaint_priority_service",
    "complaint_status_service",
    "complaint_category_mapping_service",

    # Workflow
    "workflow_definition_service",
    "workflow_step_service",
    "workflow_assignment_service",
    "workflow_history_service",
]