from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from core.database.base_model import BaseModel


class Training(BaseModel):
    __tablename__ = "trainings"

    training_order_no = Column(
        String(100),
        nullable=False,
        unique=True,
    )

    officer_id = Column(
        Integer,
        ForeignKey("officers.id"),
        nullable=False,
    )

    training_name = Column(
        String(200),
        nullable=False,
    )

    institute_name = Column(
        String(200),
        nullable=False,
    )

    start_date = Column(
        Date,
        nullable=False,
    )

    end_date = Column(
        Date,
        nullable=False,
    )

    duration_days = Column(
        Integer,
        nullable=False,
    )

    certificate_no = Column(
        String(100),
        nullable=False,
    )

    remarks = Column(
        String(300),
        nullable=True,
    )

    status = Column(
        String(30),
        nullable=False,
    )

    officer = relationship("Officer")