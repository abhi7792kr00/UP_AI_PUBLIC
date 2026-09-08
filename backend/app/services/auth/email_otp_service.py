import smtplib
from email.message import EmailMessage

from core.config.settings import settings


def send_otp_email(
    email: str,
    otp: str,
    purpose: str = "password recovery",
) -> None:
    if not settings.SMTP_HOST:
        raise ValueError("SMTP host is not configured.")

    if not settings.SMTP_USERNAME:
        raise ValueError("SMTP username is not configured.")

    if not settings.SMTP_PASSWORD:
        raise ValueError("SMTP password is not configured.")

    sender = settings.SMTP_FROM_EMAIL or settings.SMTP_USERNAME

    message = EmailMessage()
    message["Subject"] = "Union Bank Of Azamghar"
    message["From"] = sender
    message["To"] = email

    message.set_content(
        f"""Dear Citizen,

Your Bank account number XXX {purpose} is:

{otp}

This OTP is valid for 5 minutes.

Please do not share this OTP with anyone.

Regards,
UP_AI Citizen Governance Platform
"""
    )

    try:
        with smtplib.SMTP(
            settings.SMTP_HOST,
            settings.SMTP_PORT,
            timeout=30,
        ) as server:
            if settings.SMTP_USE_TLS:
                server.starttls()

            server.login(
                settings.SMTP_USERNAME,
                settings.SMTP_PASSWORD,
            )

            server.send_message(message)

    except Exception as exc:
        raise ValueError(
            f"Unable to send OTP email: {exc}"
        ) from exc
