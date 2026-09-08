from datetime import date

from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from core.database.base_model import BaseModel


class Citizen(BaseModel):
    __tablename__ = "citizens"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        unique=True,
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
        String(300),
        nullable=False,
    )

    pincode: Mapped[str | None] = mapped_column(
        String(10),
        nullable=True,
    )

    state_id: Mapped[int] = mapped_column(
        ForeignKey("states.id"),
        nullable=False,
    )

    district_id: Mapped[int] = mapped_column(
        ForeignKey("districts.id"),
        nullable=False,
    )

    tehsil_id: Mapped[int | None] = mapped_column(
        ForeignKey("tehsils.id"),
        nullable=True,
    )

    block_id: Mapped[int | None] = mapped_column(
        ForeignKey("blocks.id"),
        nullable=True,
    )

    gram_panchayat_id: Mapped[int | None] = mapped_column(
        ForeignKey("gram_panchayats.id"),
        nullable=True,
    )

    village_id: Mapped[int | None] = mapped_column(
        ForeignKey("villages.id"),
        nullable=True,
    )

    municipal_body_id: Mapped[int | None] = mapped_column(
        ForeignKey("municipal_bodies.id"),
        nullable=True,
    )

    ward_id: Mapped[int | None] = mapped_column(
        ForeignKey("wards.id"),
        nullable=True,
    )

    locality_id: Mapped[int | None] = mapped_column(
        ForeignKey("localities.id"),
        nullable=True,
    )

    user = relationship(
        "User",
    )

    state = relationship(
        "State",
    )

    district = relationship(
        "District",
    )

    tehsil = relationship(
        "Tehsil",
    )

    block = relationship(
        "Block",
    )

    gram_panchayat = relationship(
        "GramPanchayat",
    )

    village = relationship(
        "Village",
    )

    municipal_body = relationship(
        "MunicipalBody",
    )

    ward = relationship(
        "Ward",
    )

    locality = relationship(
        "Locality",
    )

    complaints = relationship(
    "Complaint",
    back_populates="citizen",
    cascade="all, delete-orphan",
    )