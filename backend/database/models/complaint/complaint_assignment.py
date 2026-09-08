from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from core.database.base_model import BaseModel


class ComplaintAssignment(BaseModel):
    __tablename__ = "complaint_assignments"

    complaint_id: Mapped[int] = mapped_column(
        ForeignKey("complaints.id"),
        nullable=False,
    )

    officer_id: Mapped[int] = mapped_column(
        ForeignKey("officers.id"),
        nullable=False,
    )

    assigned_by_officer_id: Mapped[int | None] = mapped_column(
        ForeignKey("officers.id"),
        nullable=True,
    )

    assignment_status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="Assigned",
    )

    assigned_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    accepted_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    remarks: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
    )

    complaint = relationship(
        "Complaint",
        back_populates="assignments",
    )

    officer = relationship(
        "Officer",
        foreign_keys=[officer_id],
    )

    assigned_by_officer = relationship(
        "Officer",
        foreign_keys=[assigned_by_officer_id],
    )