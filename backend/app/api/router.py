from fastapi import APIRouter

from app.api.v1.complaint.complaint_router import (
    router as complaint_router,
)

api_router = APIRouter()

api_router.include_router(
    complaint_router,
)

__all__ = [
    "api_router",
]