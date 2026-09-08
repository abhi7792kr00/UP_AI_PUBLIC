from datetime import datetime
from datetime import timedelta
from datetime import timezone

import hashlib
import hmac
import secrets

from twilio.rest import Client

from sqlalchemy.orm import Session

from core.config.settings import settings


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


def generate_otp() -> str:
    return f"{secrets.randbelow(1_000_000):06d}"


def normalize_mobile(mobile: str) -> str:
    mobile = mobile.strip().replace(" ", "")

    if mobile.startswith("+91"):
        number = mobile[3:]
    elif mobile.startswith("91") and len(mobile) == 12:
        number = mobile[2:]
    else:
        number = mobile

    if (
        len(number) != 10
        or not number.isdigit()
        or number[0] not in "6789"
    ):
        raise ValueError(
            "Enter a valid Indian mobile number."
        )

    return f"+91{number}"


def send_otp_sms(
    mobile: str,
    otp: str,
) -> None:
    if not settings.TWILIO_ACCOUNT_SID:
        raise ValueError(
            "Twilio Account SID is not configured."
        )

    if not settings.TWILIO_AUTH_TOKEN:
        raise ValueError(
            "Twilio Auth Token is not configured."
        )

    if not settings.TWILIO_PHONE_NUMBER:
        raise ValueError(
            "Twilio phone number is not configured."
        )

    client = Client(
        settings.TWILIO_ACCOUNT_SID,
        settings.TWILIO_AUTH_TOKEN,
    )

    message = client.messages.create(
        body=(
            f"Government of Uttar Pradesh citizen portal verification OTP is "
            f"{otp}. It is valid for "
            f"{OTP_EXPIRY_MINUTES} minutes."
        ),
        from_=settings.TWILIO_PHONE_NUMBER,
        to=normalize_mobile(mobile),
    )

    if not message.sid:
        raise ValueError(
            "OTP SMS could not be sent."
        )


def can_resend(
    last_otp_sent_at: datetime | None,
) -> bool:
    if last_otp_sent_at is None:
        return True

    elapsed = (
        _now() - last_otp_sent_at
    ).total_seconds()

    return elapsed >= OTP_RESEND_SECONDS
