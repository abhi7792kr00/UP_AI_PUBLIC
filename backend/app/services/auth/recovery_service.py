from datetime import datetime, timedelta
import hashlib
import hmac

from sqlalchemy.orm import Session

from database.models.auth.account_recovery import AccountRecovery
from database.models.auth.user import User

from core.config.settings import settings
from core.security.password import hash_password

from app.services.auth.citizen_otp_service import (
    generate_otp,
    normalize_mobile,
    send_otp_sms,
)

from app.services.auth.email_otp_service import (
    send_otp_email,
)


OTP_EXPIRY_MINUTES = 5
OTP_RESEND_SECONDS = 60
OTP_MAX_ATTEMPTS = 5


def _now() -> datetime:
    return datetime.utcnow()


def _hash_otp(otp: str) -> str:
    return hmac.new(
        settings.SECRET_KEY.encode(),
        otp.encode(),
        hashlib.sha256,
    ).hexdigest()


def find_user(
    db: Session,
    identifier: str,
):
    identifier = identifier.strip()

    identifier = identifier.strip()

    user = (
        db.query(User)
        .filter(
            User.username.ilike(identifier)
        )
        .first()
    )

    if user:
        return user

    user = (
        db.query(User)
        .filter(
            User.email.ilike(identifier)
        )
        .first()
    )

    if user:
        return user

    try:
        mobile = normalize_mobile(identifier)
    except ValueError:
        mobile = None

    if mobile:
        # Existing citizen records may store mobile either as
        # 10-digit number or +91-prefixed number.
        candidates = {
            mobile,
            mobile.replace("+91", "", 1),
        }

        user = (
            db.query(User)
            .filter(User.mobile.in_(candidates))
            .first()
        )

    return user


def request_password_reset(
    db: Session,
    identifier: str,
):
    user = find_user(db, identifier)

    if user is None or not user.is_active:
        raise ValueError(
            "No active account found with the provided username, email, or mobile number."
        )

    existing = (
        db.query(AccountRecovery)
        .filter(
            AccountRecovery.user_id == user.id,
            AccountRecovery.purpose == "password_reset",
            AccountRecovery.is_active == True,
        )
        .order_by(AccountRecovery.id.desc())
        .first()
    )

    now = _now()

    if (
        existing is not None
        and existing.last_otp_sent_at is not None
        and (
            now - existing.last_otp_sent_at
        ).total_seconds() < OTP_RESEND_SECONDS
    ):
        raise ValueError(
            "Please wait before requesting another OTP."
        )

    otp = generate_otp()

    if existing is None:
        recovery = AccountRecovery(
            user_id=user.id,
            purpose="password_reset",
            identifier=identifier.strip(),
            otp_hash=_hash_otp(otp),
            otp_expires_at=now + timedelta(minutes=OTP_EXPIRY_MINUTES),
            otp_attempts=0,
            last_otp_sent_at=now,
            verified=False,
            is_active=True,
        )
        db.add(recovery)
    else:
        recovery = existing
        recovery.identifier = identifier.strip()
        recovery.otp_hash = _hash_otp(otp)
        recovery.otp_expires_at = (
            now + timedelta(minutes=OTP_EXPIRY_MINUTES)
        )
        recovery.otp_attempts = 0
        recovery.last_otp_sent_at = now
        recovery.verified = False

    db.flush()

    if not user.mobile:
        db.rollback()
        raise ValueError(
            "This account does not have a registered mobile number."
        )

    try:
        identifier_clean = identifier.strip()

        # Email identifier -> send OTP by email.
        if "@" in identifier_clean:
            if not user.email:
                db.rollback()
                raise ValueError(
                    "This account does not have a registered email address."
                )

            send_otp_email(
                user.email,
                otp,
                purpose="password recovery",
            )

        # Username / mobile identifier -> send OTP by SMS.
        else:
            if not user.mobile:
                db.rollback()
                raise ValueError(
                    "This account does not have a registered mobile number."
                )

            send_otp_sms(
                user.mobile,
                otp,
            )

    except Exception as exc:
        db.rollback()
        raise ValueError(str(exc))

    db.commit()
    db.refresh(recovery)

    return recovery


def verify_recovery_otp(
    db: Session,
    recovery_id: int,
    otp: str,
):
    recovery = (
        db.query(AccountRecovery)
        .filter(
            AccountRecovery.id == recovery_id,
            AccountRecovery.is_active == True,
            AccountRecovery.purpose == "password_reset",
        )
        .first()
    )

    if recovery is None:
        raise ValueError("Recovery request not found.")

    if recovery.otp_expires_at is None:
        raise ValueError("OTP has expired.")

    now = _now()

    if now > recovery.otp_expires_at:
        raise ValueError(
            "OTP has expired. Please request a new OTP."
        )

    if recovery.otp_attempts >= OTP_MAX_ATTEMPTS:
        raise ValueError(
            "Maximum OTP attempts exceeded."
        )

    recovery.otp_attempts += 1

    expected = recovery.otp_hash or ""
    actual = _hash_otp(otp)

    if not hmac.compare_digest(expected, actual):
        db.commit()
        raise ValueError("Invalid OTP.")

    recovery.verified = True
    recovery.otp_hash = None
    recovery.otp_expires_at = None

    db.commit()
    db.refresh(recovery)

    return recovery


def reset_password(
    db: Session,
    recovery_id: int,
    new_password: str,
):
    recovery = (
        db.query(AccountRecovery)
        .filter(
            AccountRecovery.id == recovery_id,
            AccountRecovery.purpose == "password_reset",
            AccountRecovery.is_active == True,
            AccountRecovery.verified == True,
        )
        .first()
    )

    if recovery is None:
        raise ValueError(
            "Password reset verification is not valid."
        )

    user = (
        db.query(User)
        .filter(User.id == recovery.user_id)
        .first()
    )

    if user is None or not user.is_active:
        raise ValueError("User account not found.")

    user.password_hash = hash_password(new_password)

    recovery.is_active = False
    recovery.verified = False

    db.commit()

    return user


def request_username_recovery(
    db: Session,
    identifier: str,
):
    user = find_user(db, identifier)

    if user is None or not user.is_active:
        raise ValueError(
            "No active account found with the provided email or mobile number."
        )

    if not user.mobile:
        raise ValueError(
            "This account does not have a registered mobile number."
        )

    existing = (
        db.query(AccountRecovery)
        .filter(
            AccountRecovery.user_id == user.id,
            AccountRecovery.purpose == "username_recovery",
            AccountRecovery.is_active == True,
        )
        .order_by(AccountRecovery.id.desc())
        .first()
    )

    now = _now()

    if (
        existing is not None
        and existing.last_otp_sent_at is not None
        and (
            now - existing.last_otp_sent_at
        ).total_seconds() < OTP_RESEND_SECONDS
    ):
        raise ValueError(
            "Please wait before requesting another OTP."
        )

    otp = generate_otp()

    if existing is None:
        recovery = AccountRecovery(
            user_id=user.id,
            purpose="username_recovery",
            identifier=identifier.strip(),
            otp_hash=_hash_otp(otp),
            otp_expires_at=now + timedelta(minutes=OTP_EXPIRY_MINUTES),
            otp_attempts=0,
            last_otp_sent_at=now,
            verified=False,
            is_active=True,
        )
        db.add(recovery)
    else:
        recovery = existing
        recovery.identifier = identifier.strip()
        recovery.otp_hash = _hash_otp(otp)
        recovery.otp_expires_at = (
            now + timedelta(minutes=OTP_EXPIRY_MINUTES)
        )
        recovery.otp_attempts = 0
        recovery.last_otp_sent_at = now
        recovery.verified = False

    db.flush()

    try:
        identifier_clean = identifier.strip()

        if "@" in identifier_clean:
            if not user.email:
                db.rollback()
                raise ValueError(
                    "This account does not have a registered email address."
                )

            send_otp_email(
                user.email,
                otp,
                purpose="username recovery",
            )
        else:
            if not user.mobile:
                db.rollback()
                raise ValueError(
                    "This account does not have a registered mobile number."
                )

            send_otp_sms(
                user.mobile,
                otp,
            )

    except Exception as exc:
        db.rollback()
        raise ValueError(str(exc))

    db.commit()
    db.refresh(recovery)

    return recovery, user


def verify_username_recovery_otp(
    db: Session,
    recovery_id: int,
    otp: str,
):
    recovery = (
        db.query(AccountRecovery)
        .filter(
            AccountRecovery.id == recovery_id,
            AccountRecovery.purpose == "username_recovery",
            AccountRecovery.is_active == True,
        )
        .first()
    )

    if recovery is None:
        raise ValueError("Recovery request not found.")

    if recovery.otp_expires_at is None:
        raise ValueError("OTP has expired.")

    if _now() > recovery.otp_expires_at:
        raise ValueError("OTP has expired.")

    if recovery.otp_attempts >= OTP_MAX_ATTEMPTS:
        raise ValueError("Maximum OTP attempts exceeded.")

    recovery.otp_attempts += 1

    if not hmac.compare_digest(
        recovery.otp_hash or "",
        _hash_otp(otp),
    ):
        db.commit()
        raise ValueError("Invalid OTP.")

    recovery.verified = True
    recovery.otp_hash = None
    recovery.otp_expires_at = None

    db.commit()
    db.refresh(recovery)

    return recovery
