from .municipal_body import router as municipal_body_router
from .ward import router as ward_router
from .locality import router as locality_router

__all__ = [
    "municipal_body_router",
    "ward_router",
    "locality_router",
]