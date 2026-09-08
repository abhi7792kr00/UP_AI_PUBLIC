from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.dependencies.database import get_db

from app.schemas.auth.citizen_registration_schema import (
    CitizenRegistrationRequest,
    CitizenRegistrationResponse,
)

from app.services.auth.citizen_registration_service import (
    register_citizen,
)


router = APIRouter(
    prefix="/auth/citizen",
    tags=["Authentication - Citizen"],
)


@router.post(
    "/register",
    response_model=CitizenRegistrationResponse,
)
def register_new_citizen(
    request: CitizenRegistrationRequest,
    db: Session = Depends(get_db),
):
    try:
        user, citizen = register_citizen(
            db=db,
            full_name=request.full_name,
            username=request.username,
            email=request.email,
            mobile=request.mobile,
            password=request.password,
            father_name=request.father_name,
            mother_name=request.mother_name,
            gender=request.gender,
            dob=request.dob,
            address=request.address,
            pincode=request.pincode,
            state_id=request.state_id,
            district_id=request.district_id,
            area_type=request.area_type,
            tehsil_id=request.tehsil_id,
            block_id=request.block_id,
            gram_panchayat_id=request.gram_panchayat_id,
            village_id=request.village_id,
            municipal_body_id=request.municipal_body_id,
            ward_id=request.ward_id,
            locality_id=request.locality_id,
        )

    except ValueError as exc:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    except Exception:
        db.rollback()
        raise

    return CitizenRegistrationResponse(
        user_id=user.id,
        citizen_id=citizen.id,
        message="Citizen registered successfully.",
    )
