from sqlalchemy import Boolean
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from core.database.base_model import BaseModel


class WorkflowStep(BaseModel):
    """
    Represents a single step inside a workflow.

    Example:

        Complaint Workflow

            Pending
            ↓
            Verified
            ↓
            Assigned
            ↓
            In Progress
            ↓
            Resolved
            ↓
            Closed
    """

    __tablename__ = "workflow_steps"

    workflow_definition_id: Mapped[int] = mapped_column(
        ForeignKey("workflow_definitions.id"),
        nullable=False,
    )

    step_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    step_code: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    step_order: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        String(300),
        nullable=True,
    )

    is_initial: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    is_final: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    requires_assignment: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    allows_rejection: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    # ---------------------------------
    # Relationships
    # ---------------------------------

    workflow_definition = relationship(
        "WorkflowDefinition",
        back_populates="workflow_steps",
    )

    outgoing_transitions = relationship(
        "WorkflowTransition",
        foreign_keys="WorkflowTransition.from_step_id",
        back_populates="from_step",
        cascade="all, delete-orphan",
    )

    incoming_transitions = relationship(
        "WorkflowTransition",
        foreign_keys="WorkflowTransition.to_step_id",
        back_populates="to_step",
        cascade="all, delete-orphan",
    )

    workflow_history = relationship(
        "WorkflowHistory",
        back_populates="workflow_step",
    )

    workflow_assignments = relationship(
        "WorkflowAssignment",
        back_populates="workflow_step",
    )