from fastapi import APIRouter, Depends

from app.dependencies.auth import get_current_user

router = APIRouter(
    prefix="/protected",
    tags=["Protected"]
)


@router.get("/")
def protected_route(
    current_user=Depends(get_current_user)
):
    return {
        "message": "JWT Token Valid",
        "user": current_user
    }