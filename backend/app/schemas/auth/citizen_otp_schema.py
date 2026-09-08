from datetime import date

from pydantic import BaseModel, EmailStr


class CitizenOtpRequest(BaseModel):
    full_name: str
    username: str
    email: EmailStr
    mobile: str
    password: str

    father_name: str | None = None
    mother_name: str | None = None

    gender: str | None = None
    dob: date | None = None

    address: str
    pincode: str | None = None

    state_id: int
    district_id: int

    area_type: str

    tehsil_id: int | None = None
    block_id: int | None = None
    gram_panchayat_id: int | None = None
    village_id: int | None = None

    municipal_body_id: int | None = None
    ward_id: int | None = None
    locality_id: int | None = None


class CitizenOtpVerifyRequest(BaseModel):
    registration_id: int
    otp: str


class CitizenOtpResponse(BaseModel):
    registration_id: int
    message: str


class CitizenRegistrationResponse(BaseModel):
    user_id: int
    citizen_id: int
    message: str
