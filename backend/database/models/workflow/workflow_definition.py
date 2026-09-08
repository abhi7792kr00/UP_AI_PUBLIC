from sqlalchemy import Boolean
from sqlalchemy import Integer
from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from core.database.base_model import BaseModel


class WorkflowDefinition(BaseModel):
    """
    Root definition of a business workflow.

    Example:
        Complaint Workflow
        Leave Workflow
        Transfer Workflow
        Promotion Workflow
    """

    __tablename__ = "workflow_definitions"

    workflow_name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

    workflow_code: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )

    module_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        String(300),
        nullable=True,
    )

    version: Mapped[int] = mapped_column(
        Integer,
        default=1,
        nullable=False,
    )

    is_default: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    # ---------------------------------
    # Relationships
    # ---------------------------------

    workflow_steps = relationship(
        "WorkflowStep",
        back_populates="workflow_definition",
        cascade="all, delete-orphan",
    )

    workflow_history = relationship(
        "WorkflowHistory",
        back_populates="workflow_definition",
    )

    workflow_assignments = relationship(
        "WorkflowAssignment",
        back_populates="workflow_definition",
    )