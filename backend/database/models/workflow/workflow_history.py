from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from core.database.base_model import BaseModel


class WorkflowHistory(BaseModel):
    """
    Stores every workflow transition.

    Example

    Pending
        ↓
    Verified
        ↓
    Assigned
        ↓
    Resolved
    """

    __tablename__ = "workflow_history"

    workflow_definition_id: Mapped[int] = mapped_column(
        ForeignKey("workflow_definitions.id"),
        nullable=False,
    )

    workflow_step_id: Mapped[int] = mapped_column(
        ForeignKey("workflow_steps.id"),
        nullable=False,
    )

    reference_number: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    action: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    remarks: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    performed_by: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    workflow_definition = relationship(
        "WorkflowDefinition",
        back_populates="workflow_history",
    )

    workflow_step = relationship(
        "WorkflowStep",
        back_populates="workflow_history",
    )