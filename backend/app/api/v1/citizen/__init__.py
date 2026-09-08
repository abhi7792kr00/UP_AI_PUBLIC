from fastapi import APIRouter
from .citizen import router as citizen_router
from app.api.v1.citizen.citizen_complaints import (
    router as citizen_complaints_router,
)

router = APIRouter()
router.include_router(citizen_router)
router.include_router(
    citizen_complaints_router
)