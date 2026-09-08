from pydantic import BaseModel, Field


class RecoveryRequest(BaseModel):
    identifier: str = Field(min_length=3, max_length=150)


class RecoveryOtpVerifyRequest(BaseModel):
    recovery_id: int
    otp: str = Field(min_length=6, max_length=6)


class ResetPasswordRequest(BaseModel):
    recovery_id: int
    new_password: str = Field(min_length=8, max_length=128)


class RecoveryResponse(BaseModel):
    recovery_id: int
    message: str


class UsernameRecoveryResponse(BaseModel):
    recovery_id: int
    username: str
    message: str
