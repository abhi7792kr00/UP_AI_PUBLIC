from sqlalchemy.orm import Session

from app.engines.reference.reference_manager import (
    reference_manager,
)


class ReferenceEngine:
    """
    Public facade for
    reference generation.
    """

    def generate(
        self,
        db: Session,
        module_code: str,
    ) -> str:

        return (
            reference_manager.generate_reference(
                db=db,
                module_code=module_code,
            )
        )


reference_engine = (
    ReferenceEngine()
)