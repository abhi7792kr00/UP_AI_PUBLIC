from fastapi import APIRouter

from .complaint_router import (
    router as complaint_router,
)

from .complaint_category import (
    router as complaint_category_router,
)

from .complaint_subcategory import (
    router as complaint_subcategory_router,
)

from .complaint_priority import (
    router as complaint_priority_router,
)

from .complaint_status import (
    router as complaint_status_router,
)

from .complaint_feedback import (
    router as complaint_feedback_router,
)

router = APIRouter()

router.include_router(
    complaint_router,
)

router.include_router(
    complaint_category_router,
)

router.include_router(
    complaint_subcategory_router,
)

router.include_router(
    complaint_priority_router,
)

router.include_router(
    complaint_status_router,
)

router.include_router(
    complaint_feedback_router,
)