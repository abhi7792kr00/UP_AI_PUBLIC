from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.dependencies.database import get_db

from app.schemas.auth.citizen_otp_schema import (
    CitizenOtpRequest,
    CitizenOtpVerifyRequest,
    CitizenOtpResponse,
    CitizenRegistrationResponse,
)

from app.services.auth.citizen_otp_registration_service import (
    request_otp,
    verify_otp,
)


router = APIRouter(
    prefix="/auth/citizen",
    tags=["Authentication - Citizen OTP"],
)


@router.post(
    "/register/request-otp",
    response_model=CitizenOtpResponse,
)
def request_citizen_registration_otp(
    request: CitizenOtpRequest,
    db: Session = Depends(get_db),
):
    try:
        pending = request_otp(
            db,
            request,
        )

    except ValueError as exc:
        db.rollback()

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    return CitizenOtpResponse(
        registration_id=pending.id,
        message="OTP sent successfully.",
    )


@router.post(
    "/register/verify-otp",
    response_model=CitizenRegistrationResponse,
)
def verify_citizen_registration_otp(
    request: CitizenOtpVerifyRequest,
    db: Session = Depends(get_db),
):
    try:
        user, citizen = verify_otp(
            db,
            request.registration_id,
            request.otp,
        )

    except ValueError as exc:
        db.rollback()

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    return CitizenRegistrationResponse(
        user_id=user.id,
        citizen_id=citizen.id,
        message="Citizen account verified and created successfully.",
    )
