from fastapi import APIRouter, Depends

from app.dependencies.auth import require_roles

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


@router.get("/super")
def super_admin(
    current_user=Depends(
        require_roles(
            ["Super Admin"]
        )
    )
):
    return {
        "message": "Welcome Super Admin",
        "user": current_user
    }


@router.get("/district")
def district_admin(
    current_user=Depends(
        require_roles(
            [
                "Super Admin",
                "District Admin"
            ]
        )
    )
):
    return {
        "message": "District Admin Area",
        "user": current_user
    }


@router.get("/citizen")
def citizen(
    current_user=Depends(
        require_roles(
            [
                "Citizen",
                "Super Admin",
                "District Admin"
            ]
        )
    )
):
    return {
        "message": "Citizen Area",
        "user": current_user
    }