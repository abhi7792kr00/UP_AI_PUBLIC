from pydantic import BaseModel
from pydantic import Field


class ComplaintCreateRequest(BaseModel):
    """
    Complaint registration request.
    """

    # Citizen
    citizen_id: int

    # Complaint
    category_id: int
    subcategory_id: int | None = None

    subject: str = Field(
        min_length=5,
        max_length=200,
    )

    description: str = Field(
        min_length=20,
        max_length=5000,
    )

    priority_id: int | None = None

    # Location
    state_id: int
    division_id: int | None = None
    district_id: int
    tehsil_id: int | None = None
    block_id: int | None = None
    gram_panchayat_id: int | None = None
    village_id: int | None = None
    municipal_body_id: int | None = None
    ward_id: int | None = None
    locality_id: int | None = None

    address: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    pincode: str | None = None

    # Contact
    mobile_number: str | None = None
    email: str | None = None

    # Attachment
    has_attachment: bool = False

    # Metadata
    source: str = "WEB"
    language: str | None = None
    visibility: str = "PUBLIC"