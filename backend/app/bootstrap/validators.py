"""
Validator Bootstrap

Creates all validators with
their required dependencies.
"""

from app.bootstrap.repositories import (
    complaint_category_repository,
    complaint_subcategory_repository,

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
)

from app.engines.validation.basic_information_validator import (
    BasicInformationValidator,
)

from app.engines.validation.category_validator import (
    CategoryValidator,
)

from app.engines.validation.location_validator import (
    LocationValidator,
)

from app.engines.validation.contact_validator import (
    ContactValidator,
)

from app.engines.validation.attachment_validator import (
    AttachmentValidator,
)

from app.engines.validation.complaint_validator import (
    ComplaintValidator,
)

# ---------------------------------
# Individual Validators
# ---------------------------------

basic_information_validator = (
    BasicInformationValidator()
)

category_validator = (
    CategoryValidator(
        complaint_category_repository,
        complaint_subcategory_repository,
    )
)

location_validator = (
    LocationValidator(
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
    )
)

contact_validator = (
    ContactValidator()
)

attachment_validator = (
    AttachmentValidator()
)

# ---------------------------------
# Main Validator
# ---------------------------------

complaint_validator = (
    ComplaintValidator(
        complaint_category_repository,
        complaint_subcategory_repository,

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
    )
)

__all__ = [

    "basic_information_validator",

    "category_validator",

    "location_validator",

    "contact_validator",

    "attachment_validator",

    "complaint_validator",
]