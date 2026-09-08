from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db

from app.schemas.auth.recovery_schema import (
    RecoveryRequest,
    RecoveryOtpVerifyRequest,
    ResetPasswordRequest,
    RecoveryResponse,
    UsernameRecoveryResponse,
)

from app.services.auth.recovery_service import (
    request_password_reset,
    verify_recovery_otp,
    reset_password,
    request_username_recovery,
    verify_username_recovery_otp,
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication - Account Recovery"],
)


@router.post(
    "/forgot-password",
    response_model=RecoveryResponse,
)
def forgot_password(
    request: RecoveryRequest,
    db: Session = Depends(get_db),
):
    try:
        recovery = request_password_reset(
            db,
            request.identifier,
        )
    except ValueError as exc:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    return RecoveryResponse(
        recovery_id=recovery.id,
        message="OTP sent to your registered mobile number.",
    )


@router.post(
    "/forgot-password/verify-otp",
    response_model=RecoveryResponse,
)
def verify_password_reset_otp(
    request: RecoveryOtpVerifyRequest,
    db: Session = Depends(get_db),
):
    try:
        recovery = verify_recovery_otp(
            db,
            request.recovery_id,
            request.otp,
        )
    except ValueError as exc:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    return RecoveryResponse(
        recovery_id=recovery.id,
        message="OTP verified successfully.",
    )


@router.post(
    "/forgot-password/reset",
    response_model=RecoveryResponse,
)
def reset_password_endpoint(
    request: ResetPasswordRequest,
    db: Session = Depends(get_db),
):
    try:
        reset_password(
            db,
            request.recovery_id,
            request.new_password,
        )
    except ValueError as exc:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    return RecoveryResponse(
        recovery_id=request.recovery_id,
        message="Password reset successfully.",
    )


@router.post(
    "/forgot-username",
    response_model=RecoveryResponse,
)
def forgot_username(
    request: RecoveryRequest,
    db: Session = Depends(get_db),
):
    try:
        recovery, _user = request_username_recovery(
            db,
            request.identifier,
        )
    except ValueError as exc:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    return RecoveryResponse(
        recovery_id=recovery.id,
        message="OTP sent to your registered mobile number.",
    )


@router.post(
    "/forgot-username/verify-otp",
    response_model=UsernameRecoveryResponse,
)
def verify_username_otp(
    request: RecoveryOtpVerifyRequest,
    db: Session = Depends(get_db),
):
    try:
        recovery = verify_username_recovery_otp(
            db,
            request.recovery_id,
            request.otp,
        )
    except ValueError as exc:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    from database.models.auth.user import User

    user = (
        db.query(User)
        .filter(User.id == recovery.user_id)
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User account not found.",
        )

    recovery.is_active = False
    recovery.verified = False
    db.commit()

    return UsernameRecoveryResponse(
        recovery_id=recovery.id,
        username=user.username,
        message="Username recovered successfully.",
    )
