from fastapi import APIRouter

from .role import router as role_router
from .user import router as user_router
from .recovery import router as recovery_router


router = APIRouter()

router.include_router(role_router)
router.include_router(user_router)
router.include_router(recovery_router)
