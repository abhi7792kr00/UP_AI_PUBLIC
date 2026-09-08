"""
Repository Bootstrap

All repositories are instantiated here.
"""

from app.repositories.auth import (
    user_repository,
)

from app.repositories.citizen import (
    citizen_repository,
)

from app.repositories.master import (
    state_repository,
    division_repository,
    district_repository,
    tehsil_repository,
    block_repository,
    gram_panchayat_repository,
    village_repository,
    municipal_body_repository,
    ward_repository,
    locality_repository,
)

from app.repositories.complaint import (
    complaint_repository,
    complaint_category_repository,
    complaint_subcategory_repository,
    complaint_priority_repository,
    complaint_status_repository,
    complaint_category_mapping_repository,
)

from app.repositories.workflow import (
    workflow_definition_repository,
    workflow_step_repository,
    workflow_assignment_repository,
    workflow_history_repository,
)

__all__ = [
    "user_repository",

    "citizen_repository",
    "state_repository",
    "division_repository",
    "district_repository",
    "tehsil_repository",
    "block_repository",
    "gram_panchayat_repository",
    "village_repository",
    "municipal_body_repository",
    "ward_repository",
    "locality_repository",
    "complaint_repository",
    "complaint_category_repository",
    "complaint_subcategory_repository",
    "complaint_priority_repository",
    "complaint_status_repository",
    "complaint_category_mapping_repository",

    "workflow_definition_repository",
    "workflow_step_repository",
    "workflow_assignment_repository",
    "workflow_history_repository",
]