from typing import Optional

from app.common.enums import (
    AddressType,
    ComplaintSource,
    ComplaintVisibility,
)

from pydantic import BaseModel


class ComplaintRegistrationRequest(
    BaseModel
):
    """
    Enterprise DTO

    Complaint Registration Request

    Shared between

    • Workflow

    • Address Resolver

    • Jurisdiction Engine

    • Routing Engine

    • Priority Engine

    • Assignment Engine

    • Tracking Engine

    • Timeline Engine
    """

    # ---------------------------------
    # Citizen
    # ---------------------------------

    citizen_id: int

    mobile: Optional[str] = None

    language: Optional[str] = None

    # ---------------------------------
    # Complaint
    # ---------------------------------

    category_id: int

    subcategory_id: int

    subject: str

    description: str

    # ---------------------------------
    # Address
    # ---------------------------------

    address_type: AddressType

    state_id: int

    division_id: int

    district_id: int

    tehsil_id: Optional[int] = None

    block_id: Optional[int] = None

    gram_panchayat_id: Optional[int] = None

    village_id: Optional[int] = None

    municipal_body_id: Optional[int] = None

    ward_id: Optional[int] = None

    locality_id: Optional[int] = None

    address: Optional[str] = None

    landmark: Optional[str] = None

    pincode: Optional[str] = None

    latitude: Optional[float] = None

    longitude: Optional[float] = None

    # ---------------------------------
    # Evidence
    # ---------------------------------

    photo_count: int = 0

    video_count: int = 0

    audio_count: int = 0

    document_count: int = 0

    # ---------------------------------
    # Visibility
    # ---------------------------------

    visibility: ComplaintVisibility = ComplaintVisibility.PRIVATE

    anonymous: bool = False

    # ---------------------------------
    # Source
    # ---------------------------------

    source: ComplaintSource = ComplaintSource.WEB

    device: Optional[str] = None

    app_version: Optional[str] = None

    ip_address: Optional[str] = None

    # ---------------------------------
    # Verification
    # ---------------------------------

    otp_verified: bool = False