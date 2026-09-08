from sqlalchemy.orm import Session

from app.common.validation.validation_result import (
    ValidationResult,
)

from app.dto.complaint.complaint_request import (
    ComplaintRequest,
)

from app.engines.base.base_engine import (
    BaseEngine,
)


class LocationValidator(BaseEngine):
    """
    Validates the administrative location
    hierarchy of a complaint.
    """

    def __init__(
        self,
        state_repository,
        division_repository,
        district_repository,
        tehsil_repository,
        block_repository,
        gram_panchayat_repository,
        village_repository,
        municipal_body_repository,
        ward_repository,
        locality_repository,
    ):
        self.state_repository = state_repository
        self.division_repository = division_repository
        self.district_repository = district_repository
        self.tehsil_repository = tehsil_repository
        self.block_repository = block_repository
        self.gram_panchayat_repository = gram_panchayat_repository
        self.village_repository = village_repository
        self.municipal_body_repository = municipal_body_repository
        self.ward_repository = ward_repository
        self.locality_repository = locality_repository

    def validate(
        self,
        db: Session,
        request: ComplaintRequest,
        result: ValidationResult,
    ) -> None:
        """
        Validate complaint location.

        Detailed hierarchy validation
        will be implemented incrementally.
        """

        self.validate_state(
            db,
            request,
            result,
        )

        self.validate_district(
            db,
            request,
            result,
        )

    def validate_state(
        self,
        db: Session,
        request: ComplaintRequest,
        result: ValidationResult,
    ) -> None:

        state = self.state_repository.get_by_id(
            db,
            request.state_id,
        )

        if state is None:
            result.add_error(
                field="state_id",
                error_code="INVALID_STATE",
                message="Selected state does not exist.",
            )

    def validate_district(
        self,
        db: Session,
        request: ComplaintRequest,
        result: ValidationResult,
    ) -> None:

        district = self.district_repository.get_by_id(
            db,
            request.district_id,
        )

        if district is None:
            result.add_error(
                field="district_id",
                error_code="INVALID_DISTRICT",
                message="Selected district does not exist.",
            )