from datetime import datetime

from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Numeric
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from core.database.base_model import BaseModel


class Complaint(BaseModel):
    __tablename__ = "complaints"

    complaint_number: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )

    # -------------------------
    # Citizen
    # -------------------------

    citizen_id: Mapped[int] = mapped_column(
        ForeignKey("citizens.id"),
        nullable=False,
    )

    # -------------------------
    # Complaint Masters
    # -------------------------

    category_id: Mapped[int] = mapped_column(
        ForeignKey("complaint_categories.id"),
        nullable=False,
    )

    priority_id: Mapped[int] = mapped_column(
        ForeignKey("complaint_priorities.id"),
        nullable=False,
    )

    status_id: Mapped[int] = mapped_column(
        ForeignKey("complaint_statuses.id"),
        nullable=False,
    )

    # -------------------------
    # Routing
    # -------------------------

    department_id: Mapped[int] = mapped_column(
        ForeignKey("departments.id"),
        nullable=False,
    )

    office_id: Mapped[int] = mapped_column(
        ForeignKey("offices.id"),
        nullable=False,
    )

    assigned_officer_id: Mapped[int | None] = mapped_column(
        ForeignKey("officers.id"),
        nullable=True,
    )

    # -------------------------
    # Complaint Details
    # -------------------------

    subject: Mapped[str] = mapped_column(
        String(250),
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        String(5000),
        nullable=False,
    )

    # -------------------------
    # Location
    # -------------------------

    address: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    latitude: Mapped[float | None] = mapped_column(
        Numeric(10, 7),
        nullable=True,
    )

    longitude: Mapped[float | None] = mapped_column(
        Numeric(10, 7),
        nullable=True,
    )

    # -------------------------
    # Tracking
    # -------------------------

    due_date: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    closed_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    # -------------------------
    # Verification
    # -------------------------

    is_otp_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    # -------------------------
    # Visibility
    # -------------------------

    is_public: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    # -------------------------
    # Source
    # -------------------------

    source: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
    )

    language: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
    )

    # -------------------------
    # Relationships
    # -------------------------

    citizen = relationship(
        "Citizen",
        back_populates="complaints",
    )

    category = relationship(
        "ComplaintCategory",
        back_populates="complaints",
    )

    priority = relationship(
        "ComplaintPriority",
        back_populates="complaints",
    )

    status = relationship(
        "ComplaintStatus",
        back_populates="complaints",
    )

    department = relationship(
        "Department",
    )

    office = relationship(
        "Office",
    )

    assigned_officer = relationship(
        "Officer",
    )

    assignments = relationship(
        "ComplaintAssignment",
        back_populates="complaint",
        cascade="all, delete-orphan",
    )

    timelines = relationship(
        "ComplaintTimeline",
        back_populates="complaint",
        cascade="all, delete-orphan",
    )

    attachments = relationship(
        "ComplaintAttachment",
        back_populates="complaint",
        cascade="all, delete-orphan",
    )

    escalations = relationship(
        "ComplaintEscalation",
        back_populates="complaint",
        cascade="all, delete-orphan",
    )

    feedbacks = relationship(
        "ComplaintFeedback",
        back_populates="complaint",
        cascade="all, delete-orphan",
    )

    otps = relationship(
        "ComplaintOTP",
        back_populates="complaint",
        cascade="all, delete-orphan",
    )

    subcategory_id: Mapped[int | None] = mapped_column(
    ForeignKey("complaint_subcategories.id"),
    nullable=True,
    )

    subcategory = relationship(
    "ComplaintSubCategory",
    back_populates="complaints",
    )