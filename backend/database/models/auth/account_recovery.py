from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from core.database.base_model import BaseModel


class AccountRecovery(BaseModel):
    __tablename__ = "account_recoveries"

    user_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        index=True,
    )

    purpose: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    identifier: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    otp_hash: Mapped[str | None] = mapped_column(
        String(128),
        nullable=True,
    )

    otp_expires_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    otp_attempts: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    last_otp_sent_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )
