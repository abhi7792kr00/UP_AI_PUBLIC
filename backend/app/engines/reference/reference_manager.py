from datetime import datetime

from sqlalchemy.orm import Session

from app.engines.reference.reference_formatter import (
    reference_formatter,
)
from app.engines.reference.reference_generator import (
    reference_generator,
)

from app.repositories.reference.reference_format_repository import (
    reference_format_repository,
)

from app.repositories.reference.reference_sequence_repository import (
    reference_sequence_repository,
)

from app.repositories.reference.reference_type_repository import (
    reference_type_repository,
)


class ReferenceManager:
    """
    Coordinates the complete
    reference generation workflow.
    """

    def generate_reference(
        self,
        db: Session,
        module_code: str,
    ) -> str:

        # =====================================
        # Rule-001
        # Reference Type must exist
        # =====================================

        reference_type = (
            reference_type_repository.get_by_module_code(
                db,
                module_code,
            )
        )

        if reference_type is None:
            raise ValueError(
                f"Reference type '{module_code}' not found."
            )

        # =====================================
        # Rule-002
        # Reference Type must be active
        # =====================================

        if not reference_type.is_active:
            raise ValueError(
                f"Reference type '{module_code}' is inactive."
            )

        # =====================================
        # Rule-003
        # Exactly one active format
        # =====================================

        reference_formats = (
            reference_format_repository.get_active_by_type(
                db,
                reference_type.id,
            )
        )

        if len(reference_formats) == 0:
            raise ValueError(
                f"No active reference format configured "
                f"for '{module_code}'."
            )

        if len(reference_formats) > 1:
            raise ValueError(
                f"Multiple active reference formats found "
                f"for '{module_code}'."
            )

        reference_format = reference_formats[0]

        # =====================================
        # Determine current period
        # (Version-1 : YEAR)
        # =====================================

        sequence_period = "YEAR"

        period_value = str(
            datetime.now().year
        )

        # =====================================
        # Find sequence
        # =====================================

        sequence = (
            reference_sequence_repository
            .get_by_format_and_period(
                db=db,
                reference_format_id=reference_format.id,
                sequence_period=sequence_period,
                period_value=period_value,
            )
        )

        # =====================================
        # Rule-004
        # Auto create sequence
        # =====================================

        if sequence is None:

            sequence = (
                reference_sequence_repository
                .create_initial_sequence(
                    db=db,
                    reference_format_id=reference_format.id,
                    sequence_period=sequence_period,
                    period_value=period_value,
                )
            )

        # =====================================
        # Rule-005
        # Generate next sequence
        # =====================================

        next_sequence = (
            reference_generator.next_sequence(
                sequence.current_sequence
            )
        )

        # =====================================
        # Rule-006
        # Persist sequence
        # =====================================

        reference_sequence_repository.update_sequence(
            db=db,
            sequence=sequence,
            next_sequence=next_sequence,
        )

        # =====================================
        # Rule-007
        # Format reference
        # =====================================

        reference_number = (
            reference_formatter.format(
                prefix=reference_format.prefix,
                separator=reference_format.separator,
                period_value=period_value,
                sequence=next_sequence,
                sequence_length=reference_format.sequence_length,
            )
        )

        # =====================================
        # Return
        # =====================================

        return reference_number


reference_manager = (
    ReferenceManager()
)