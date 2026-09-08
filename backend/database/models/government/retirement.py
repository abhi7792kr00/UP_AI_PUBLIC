from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from core.database.base_model import BaseModel


class Retirement(BaseModel):
    __tablename__ = "retirements"

    retirement_order_no = Column(String(100), unique=True, nullable=False)

    retirement_date = Column(Date, nullable=False)

    officer_id = Column(
        Integer,
        ForeignKey("officers.id"),
        nullable=False,
    )

    retirement_type = Column(
        String(100),
        nullable=False,
    )

    age_at_retirement = Column(
        Integer,
        nullable=False,
    )

    pension_status = Column(
        String(50),
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