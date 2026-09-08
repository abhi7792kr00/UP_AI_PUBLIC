from datetime import datetime

from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from core.database.base_model import BaseModel


class ComplaintEscalation(BaseModel):
    __tablename__ = "complaint_escalations"

    complaint_id: Mapped[int] = mapped_column(
        ForeignKey("complaints.id"),
        nullable=False,
    )

    from_officer_id: Mapped[int | None] = mapped_column(
        ForeignKey("officers.id"),
        nullable=True,
    )

    to_officer_id: Mapped[int] = mapped_column(
        ForeignKey("officers.id"),
        nullable=False,
    )

    reason: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    escalation_level: Mapped[int] = mapped_column(
        nullable=False,
        default=1,
    )

    is_auto: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    escalated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    complaint = relationship(
        "Complaint",
        back_populates="escalations",
    )

    from_officer = relationship(
        "Officer",
        foreign_keys=[from_officer_id],
    )

    to_officer = relationship(
        "Officer",
        foreign_keys=[to_officer_id],
    )