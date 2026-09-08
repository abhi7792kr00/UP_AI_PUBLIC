from sqlalchemy import Boolean
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from core.database.base_model import BaseModel


class WorkflowAssignment(BaseModel):
    """
    Stores assignment information
    for workflow execution.
    """

    __tablename__ = "workflow_assignments"

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

    assigned_to: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    assigned_by: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    assignment_type: Mapped[str] = mapped_column(
        String(50),
        default="MANUAL",
        nullable=False,
    )

    remarks: Mapped[str | None] = mapped_column(
        String(300),
        nullable=True,
    )

    is_completed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    workflow_definition = relationship(
        "WorkflowDefinition",
        back_populates="workflow_assignments",
    )

    workflow_step = relationship(
        "WorkflowStep",
        back_populates="workflow_assignments",
    )