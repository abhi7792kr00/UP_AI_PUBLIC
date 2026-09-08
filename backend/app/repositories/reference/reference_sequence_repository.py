from datetime import datetime

from sqlalchemy.orm import Session

from app.repositories.base.base_repository import BaseRepository

from database.models.reference.reference_sequence import (
    ReferenceSequence,
)


class ReferenceSequenceRepository(
    BaseRepository[ReferenceSequence]
):
    def __init__(self):
        super().__init__(
            ReferenceSequence
        )

    # ---------------------------------
    # Query Methods
    # ---------------------------------

    def get_by_format_and_period(
        self,
        db: Session,
        reference_format_id: int,
        sequence_period: str,
        period_value: str,
    ) -> ReferenceSequence | None:
        return (
            db.query(
                ReferenceSequence
            )
            .filter(
                ReferenceSequence.reference_format_id
                == reference_format_id,
                ReferenceSequence.sequence_period
                == sequence_period,
                ReferenceSequence.period_value
                == period_value,
            )
            .first()
        )

    # ---------------------------------
    # Create Methods
    # ---------------------------------

    def create_initial_sequence(
        self,
        db: Session,
        reference_format_id: int,
        sequence_period: str,
        period_value: str,
    ) -> ReferenceSequence:

        sequence = ReferenceSequence(
            reference_format_id=reference_format_id,
            sequence_period=sequence_period,
            period_value=period_value,
            current_sequence=0,
            last_generated_at=None,
        )

        db.add(sequence)
        db.commit()
        db.refresh(sequence)

        return sequence

    # ---------------------------------
    # Update Methods
    # ---------------------------------

    def update_sequence(
        self,
        db: Session,
        sequence: ReferenceSequence,
        next_sequence: int,
    ) -> ReferenceSequence:

        sequence.current_sequence = next_sequence
        sequence.last_generated_at = datetime.utcnow()

        db.commit()
        db.refresh(sequence)

        return sequence

    # ---------------------------------
    # Transaction Methods
    # ---------------------------------

    def get_sequence_for_update(
        self,
        db: Session,
        reference_format_id: int,
        sequence_period: str,
        period_value: str,
    ) -> ReferenceSequence | None:
        """
        Reserved for transaction-safe
        sequence generation.

        Future implementation may use
        SELECT ... FOR UPDATE
        depending on the database backend.
        """

        return (
            db.query(
                ReferenceSequence
            )
            .filter(
                ReferenceSequence.reference_format_id
                == reference_format_id,
                ReferenceSequence.sequence_period
                == sequence_period,
                ReferenceSequence.period_value
                == period_value,
            )
            .first()
        )


reference_sequence_repository = (
    ReferenceSequenceRepository()
)