from sqlalchemy import Boolean
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from core.database.base_model import BaseModel


class ComplaintFeedback(BaseModel):
    __tablename__ = "complaint_feedbacks"

    complaint_id: Mapped[int] = mapped_column(
        ForeignKey("complaints.id"),
        nullable=False,
    )

    citizen_id: Mapped[int] = mapped_column(
        ForeignKey("citizens.id"),
        nullable=False,
    )

    rating: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    feedback_text: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
    )

    is_satisfied: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    complaint = relationship(
        "Complaint",
        back_populates="feedbacks",
    )

    citizen = relationship(
        "Citizen",
    )