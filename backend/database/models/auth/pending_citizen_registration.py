from datetime import date
from datetime import datetime

from sqlalchemy import Date
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from core.database.base_model import BaseModel


class PendingCitizenRegistration(BaseModel):
    __tablename__ = "pending_citizen_registrations"

    full_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    username: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    mobile: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    father_name: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    mother_name: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    gender: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    dob: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    address: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    pincode: Mapped[str | None] = mapped_column(
        String(10),
        nullable=True,
    )

    state_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    district_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    area_type: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    tehsil_id: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    block_id: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    gram_panchayat_id: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    village_id: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    municipal_body_id: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    ward_id: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    locality_id: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
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
