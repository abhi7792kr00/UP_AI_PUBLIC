from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from core.database.base_model import BaseModel


class ComplaintTimeline(BaseModel):
    __tablename__ = "complaint_timelines"

    complaint_id: Mapped[int] = mapped_column(
        ForeignKey("complaints.id"),
        nullable=False,
    )

    officer_id: Mapped[int | None] = mapped_column(
        ForeignKey("officers.id"),
        nullable=True,
    )

    status_id: Mapped[int | None] = mapped_column(
        ForeignKey("complaint_statuses.id"),
        nullable=True,
    )

    action: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    remarks: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
    )

    ip_address: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    device_info: Mapped[str | None] = mapped_column(
        String(300),
        nullable=True,
    )

    complaint = relationship(
        "Complaint",
        back_populates="timelines",
    )

    officer = relationship(
        "Officer",
    )

    status = relationship(
        "ComplaintStatus",
    )