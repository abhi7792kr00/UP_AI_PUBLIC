from pydantic import BaseModel, Field


class ComplaintTransitionRequest(BaseModel):
    to_status_id: int = Field(
        ...,
        description="Target complaint status ID",
        examples=[2],
    )

    remarks: str | None = Field(
        default=None,
        description="Remarks for this workflow transition",
        examples=["Complaint assigned to concerned officer"],
    )

    performed_by: int | None = Field(
        default=None,
        description="Officer/user who performed the transition",
        examples=[1],
    )
