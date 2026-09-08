from sqlalchemy.orm import Session

from app.engines.base.base_engine import (
    BaseEngine,
)

from app.repositories.government import (
    officer_repository,
)


class OfficerResolver(BaseEngine):
    """
    Resolves the officer responsible
    for a complaint based on routing.
    """

    def resolve(
        self,
        db: Session,
        *,
        department_id: int,
        designation_id: int,
        office_id: int,
    ):
        officer = (
            officer_repository.get_matching_officer(
                db=db,
                department_id=department_id,
                designation_id=designation_id,
                office_id=office_id,
            )
        )

        if officer is None:
            raise ValueError(
                "No active officer found for "
                "the complaint routing."
            )

        return officer


officer_resolver = OfficerResolver()
