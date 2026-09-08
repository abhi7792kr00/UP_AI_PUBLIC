from datetime import timedelta

from sqlalchemy.orm import Session

from app.repositories.auth.user_repository import user_repository

from app.services.auth.citizen_otp_service import (
    OTP_EXPIRY_MINUTES,
    OTP_MAX_ATTEMPTS,
    _hash_otp,
    _now,
    can_resend,
    generate_otp,
    send_otp_sms,
)

from core.security.password import hash_password

from database.models.auth.pending_citizen_registration import (
    PendingCitizenRegistration,
)

from database.models.auth.user import User
from database.models.citizen.citizen import Citizen


CITIZEN_ROLE_ID = 9


def request_otp(
    db: Session,
    request,
):
    if user_repository.get_by_username(
        db,
        request.username,
    ):
        raise ValueError(
            "Username already exists."
        )

    if user_repository.get_by_email(
        db,
        request.email,
    ):
        raise ValueError(
            "Email already exists."
        )

    if user_repository.get_by_mobile(
        db,
        request.mobile,
    ):
        raise ValueError(
            "Mobile already exists."
        )

    area_type = request.area_type.strip().lower()

    if area_type not in {
        "rural",
        "urban",
    }:
        raise ValueError(
            "area_type must be rural or urban."
        )

    if area_type == "rural":
        municipal_body_id = None
        ward_id = None
        locality_id = None
    else:
        tehsil_id = None
        block_id = None
        gram_panchayat_id = None
        village_id = None

    pending = (
        db.query(
            PendingCitizenRegistration
        )
        .filter(
            PendingCitizenRegistration.mobile
            == request.mobile
        )
        .first()
    )

    now = _now()

    if pending is not None:
        if not can_resend(
            pending.last_otp_sent_at
        ):
            raise ValueError(
                "Please wait before requesting another OTP."
            )

        pending.full_name = request.full_name
        pending.username = request.username
        pending.email = request.email
        pending.password_hash = hash_password(
            request.password
        )

        pending.father_name = request.father_name
        pending.mother_name = request.mother_name
        pending.gender = request.gender
        pending.dob = request.dob

        pending.address = request.address
        pending.pincode = request.pincode

        pending.state_id = request.state_id
        pending.district_id = request.district_id
        pending.area_type = area_type

        pending.tehsil_id = request.tehsil_id
        pending.block_id = request.block_id
        pending.gram_panchayat_id = request.gram_panchayat_id
        pending.village_id = request.village_id

        pending.municipal_body_id = municipal_body_id
        pending.ward_id = ward_id
        pending.locality_id = locality_id

        pending.otp_attempts = 0
    else:
        pending = PendingCitizenRegistration(
            full_name=request.full_name,
            username=request.username,
            email=request.email,
            mobile=request.mobile,
            password_hash=hash_password(
                request.password
            ),
            father_name=request.father_name,
            mother_name=request.mother_name,
            gender=request.gender,
            dob=request.dob,
            address=request.address,
            pincode=request.pincode,
            state_id=request.state_id,
            district_id=request.district_id,
            area_type=area_type,
            tehsil_id=request.tehsil_id,
            block_id=request.block_id,
            gram_panchayat_id=request.gram_panchayat_id,
            village_id=request.village_id,
            municipal_body_id=municipal_body_id,
            ward_id=ward_id,
            locality_id=locality_id,
            otp_attempts=0,
        )

        db.add(pending)

    db.flush()

    otp = generate_otp()

    pending.otp_hash = _hash_otp(otp)
    pending.otp_expires_at = (
        now + timedelta(
            minutes=OTP_EXPIRY_MINUTES
        )
    )
    pending.last_otp_sent_at = now
    pending.otp_attempts = 0

    try:
        send_otp_sms(
            request.mobile,
            otp,
        )
    except Exception:
        db.rollback()
        raise ValueError(
            "Unable to send OTP. Please try again."
        )

    db.commit()
    db.refresh(pending)

    return pending


def verify_otp(
    db: Session,
    registration_id: int,
    otp: str,
):
    pending = (
        db.query(
            PendingCitizenRegistration
        )
        .filter(
            PendingCitizenRegistration.id
            == registration_id,
            PendingCitizenRegistration.is_active
            == True,
        )
        .first()
    )

    if pending is None:
        raise ValueError(
            "Registration request not found."
        )

    now = _now()

    if (
        pending.otp_expires_at is None
        or now > pending.otp_expires_at
    ):
        raise ValueError(
            "OTP has expired. Please request a new OTP."
        )

    if pending.otp_attempts >= OTP_MAX_ATTEMPTS:
        raise ValueError(
            "Maximum OTP attempts exceeded."
        )

    pending.otp_attempts += 1

    expected_hash = pending.otp_hash or ""
    actual_hash = _hash_otp(otp)

    if actual_hash != expected_hash:
        db.commit()

        raise ValueError(
            "Invalid OTP."
        )

    existing_user = (
        db.query(User)
        .filter(
            User.username == pending.username,
        )
        .first()
    )

    if existing_user is not None:
        db.rollback()
        raise ValueError(
            "Username already exists."
        )

    existing_email = (
        db.query(User)
        .filter(
            User.email == pending.email,
        )
        .first()
    )

    if existing_email is not None:
        db.rollback()
        raise ValueError(
            "Email already exists."
        )

    existing_mobile = (
        db.query(User)
        .filter(
            User.mobile == pending.mobile,
        )
        .first()
    )

    if existing_mobile is not None:
        db.rollback()
        raise ValueError(
            "Mobile already exists."
        )

    user = User(
        full_name=pending.full_name,
        username=pending.username,
        email=pending.email,
        password_hash=pending.password_hash,
        mobile=pending.mobile,
        role_id=CITIZEN_ROLE_ID,
        officer_id=None,
    )

    db.add(user)
    db.flush()

    citizen = Citizen(
        user_id=user.id,
        father_name=pending.father_name,
        mother_name=pending.mother_name,
        gender=pending.gender,
        dob=pending.dob,
        address=pending.address,
        pincode=pending.pincode,
        state_id=pending.state_id,
        district_id=pending.district_id,
        tehsil_id=pending.tehsil_id,
        block_id=pending.block_id,
        gram_panchayat_id=pending.gram_panchayat_id,
        village_id=pending.village_id,
        municipal_body_id=pending.municipal_body_id,
        ward_id=pending.ward_id,
        locality_id=pending.locality_id,
    )

    db.add(citizen)

    pending.is_active = False
    pending.otp_hash = None
    pending.otp_expires_at = None

    db.commit()

    db.refresh(user)
    db.refresh(citizen)

    return user, citizen
