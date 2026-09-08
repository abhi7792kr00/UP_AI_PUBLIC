from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.auth.login_schema import LoginRequest
from app.services.auth.auth_service import login
from app.dependencies.current_user import get_current_user
from database.models.auth.user import User
from database.models.citizen.citizen import Citizen


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/login")
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    result = login(
        db,
        form_data.username,
        form_data.password
    )

    if result is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    return result
@router.get("/me")
def get_me(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    result = {
        "id": current_user.id,
        "full_name": current_user.full_name,
        "username": current_user.username,
        "email": current_user.email,
        "mobile": current_user.mobile,
        "is_active": current_user.is_active,
        "role_id": current_user.role_id,
        "citizen": None,
    }

    if current_user.role_id == 9:
        citizen = (
            db.query(Citizen)
            .filter(
                Citizen.user_id == current_user.id,
                Citizen.is_active == True,
            )
            .first()
        )

        if citizen is not None:
            area_type = (
                "urban"
                if citizen.municipal_body_id is not None
                else "rural"
            )

            result["citizen"] = {
                "id": citizen.id,
                "father_name": citizen.father_name,
                "mother_name": citizen.mother_name,
                "gender": citizen.gender,
                "dob": citizen.dob,
                "address": citizen.address,
                "pincode": citizen.pincode,

                "state_id": citizen.state_id,
                "district_id": citizen.district_id,

                "area_type": area_type,

                "tehsil_id": citizen.tehsil_id,
                "block_id": citizen.block_id,
                "gram_panchayat_id": citizen.gram_panchayat_id,
                "village_id": citizen.village_id,

                "municipal_body_id": citizen.municipal_body_id,
                "ward_id": citizen.ward_id,
                "locality_id": citizen.locality_id,
            }

    return result