from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database.base_model import BaseModel



class Office(BaseModel):
    __tablename__ = "offices"

    office_name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    office_code: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )

    address: Mapped[str] = mapped_column(
        String(300),
        nullable=True,
    )

    phone: Mapped[str] = mapped_column(
        String(20),
        nullable=True,
    )

    email: Mapped[str] = mapped_column(
        String(150),
        nullable=True,
    )

    department_id: Mapped[int] = mapped_column(
        ForeignKey("departments.id"),
        nullable=False,
    )

    district_id: Mapped[int | None] = mapped_column(
        ForeignKey("districts.id"),
        nullable=True,
    )

    tehsil_id: Mapped[int | None] = mapped_column(
        ForeignKey("tehsils.id"),
        nullable=True,
    )

    block_id: Mapped[int | None] = mapped_column(
        ForeignKey("blocks.id"),
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

    department = relationship(
        "Department",
        back_populates="offices",
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

    municipal_body = relationship(
        "MunicipalBody",
    )

    ward = relationship(
        "Ward",
    )

    locality = relationship(
        "Locality",
    )

    officers = relationship(
        "Officer",
        back_populates="office",
    )    

    postings = relationship(
        "Posting",
        back_populates="office",
    )