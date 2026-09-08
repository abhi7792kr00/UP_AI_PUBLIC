from enum import Enum

from sqlalchemy import Enum as SqlEnum
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from core.database.base_model import BaseModel


class MunicipalBodyType(str, Enum):
    NAGAR_NIGAM = "NAGAR_NIGAM"
    NAGAR_PALIKA_PARISHAD = "NAGAR_PALIKA_PARISHAD"
    NOTIFIED_AREA_COUNCIL = "NOTIFIED_AREA_COUNCIL"
    NAGAR_PANCHAYAT = "NAGAR_PANCHAYAT"
    CANTONMENT_BOARD = "CANTONMENT_BOARD"


class MunicipalBody(BaseModel):
    __tablename__ = "municipal_bodies"

    # ---------------------------------
    # Basic Information
    # ---------------------------------

    body_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    body_code: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False,
    )

    body_type: Mapped[MunicipalBodyType] = mapped_column(
        SqlEnum(MunicipalBodyType),
        nullable=False,
    )

    # ---------------------------------
    # Administrative Hierarchy
    # ---------------------------------

    district_id: Mapped[int] = mapped_column(
        ForeignKey("districts.id"),
        nullable=False,
    )

    # ---------------------------------
    # Office Details
    # ---------------------------------

    headquarters: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True,
    )

    # ---------------------------------
    # Relationships
    # ---------------------------------

    district = relationship(
        "District",
        back_populates="municipal_bodies",
    )

    wards = relationship(
        "Ward",
        back_populates="municipal_body",
        cascade="all, delete-orphan",
    )