from sqlalchemy.orm import Session

from app.dto.complaint.complaint_registration_request import (
    ComplaintRegistrationRequest,
)


class AddressResolver:
    """
    Enterprise Address Resolver

    Responsibilities

    1. Detect Rural / Urban

    2. Validate Administrative Hierarchy

    3. Normalize Address

    4. Return Resolved Address
    """

    def __init__(self):
        pass

    def resolve(
        self,
        db: Session,
        request: ComplaintRegistrationRequest,
    ):
        """
        Resolve Complaint Address

        Future Steps

        1. Detect Address Type

        2. Validate State

        3. Validate Division

        4. Validate District

        5. Validate Rural / Urban Hierarchy

        6. Normalize Address

        7. Return Resolved Address DTO
        """

        if request.address_type.value == "RURAL":

            return {
                "address_type": request.address_type,
                "state_id": request.state_id,
                "division_id": request.division_id,
                "district_id": request.district_id,
                "tehsil_id": request.tehsil_id,
                "block_id": request.block_id,
                "gram_panchayat_id": request.gram_panchayat_id,
                "village_id": request.village_id,
            }

        return {
            "address_type": request.address_type,
            "state_id": request.state_id,
            "division_id": request.division_id,
            "district_id": request.district_id,
            "municipal_body_id": request.municipal_body_id,
            "ward_id": request.ward_id,
            "locality_id": request.locality_id,
        }


address_resolver = AddressResolver()