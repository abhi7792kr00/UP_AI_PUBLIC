from sqlalchemy import Boolean
from sqlalchemy import ForeignKey
from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from core.database.base_model import BaseModel


class WorkflowTransition(BaseModel):
    """
    Represents an allowed transition
    between two workflow steps.

    Example

    Pending
        ↓
    Verified

    Verified
        ↓
    Assigned
    """

    __tablename__ = "workflow_transitions"

    workflow_definition_id: Mapped[int] = mapped_column(
        ForeignKey("workflow_definitions.id"),
        nullable=False,
    )

    from_step_id: Mapped[int] = mapped_column(
        ForeignKey("workflow_steps.id"),
        nullable=False,
    )

    to_step_id: Mapped[int] = mapped_column(
        ForeignKey("workflow_steps.id"),
        nullable=False,
    )

    transition_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    transition_code: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True,
    )

    description: Mapped[str | None] = mapped_column(
        String(300),
        nullable=True,
    )

    requires_remark: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    requires_attachment: Mapped[bool] = mapped_column(
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

    workflow_definition = relationship(
        "WorkflowDefinition",
    )

    from_step = relationship(
        "WorkflowStep",
        foreign_keys=[from_step_id],
        back_populates="outgoing_transitions",
    )

    to_step = relationship(
        "WorkflowStep",
        foreign_keys=[to_step_id],
        back_populates="incoming_transitions",
    )