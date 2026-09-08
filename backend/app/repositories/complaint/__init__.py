from app.repositories.complaint.complaint_repository import (
    ComplaintRepository,
    complaint_repository,
)

from app.repositories.complaint.complaint_category_repository import (
    ComplaintCategoryRepository,
    complaint_category_repository,
)

from app.repositories.complaint.complaint_subcategory_repository import (
    ComplaintSubCategoryRepository,
    complaint_subcategory_repository,
)

from app.repositories.complaint.complaint_priority_repository import (
    ComplaintPriorityRepository,
    complaint_priority_repository,
)

from app.repositories.complaint.complaint_status_repository import (
    ComplaintStatusRepository,
    complaint_status_repository,
)

from app.repositories.complaint.complaint_category_mapping_repository import (
    ComplaintCategoryMappingRepository,
    complaint_category_mapping_repository,
)
__all__ = [
    "ComplaintRepository",
    "complaint_repository",
    "ComplaintCategoryRepository",
    "complaint_category_repository",
    "ComplaintSubCategoryRepository",
    "complaint_subcategory_repository",
    "ComplaintPriorityRepository",
    "complaint_priority_repository",
    "ComplaintCategoryMappingRepository",
    "complaint_category_mapping_repository",
]