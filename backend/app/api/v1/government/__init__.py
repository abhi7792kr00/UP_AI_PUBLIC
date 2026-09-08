from fastapi import APIRouter

from .dashboard import router as dashboard_router
from .department import router as department_router
from .designation import router as designation_router
from .leave import router as leave_router
from .office import router as office_router
from .officer import router as officer_router
from .posting import router as posting_router
from .promotion import router as promotion_router
from .retirement import router as retirement_router
from .service_history import router as service_history_router
from .suspension import router as suspension_router
from .training import router as training_router
from .transfer import router as transfer_router


router = APIRouter()

router.include_router(department_router)
router.include_router(designation_router)
router.include_router(officer_router)
router.include_router(office_router)
router.include_router(posting_router)
router.include_router(transfer_router)
router.include_router(promotion_router)
router.include_router(leave_router)
router.include_router(suspension_router)
router.include_router(retirement_router)
router.include_router(training_router)
router.include_router(dashboard_router)
router.include_router(service_history_router)