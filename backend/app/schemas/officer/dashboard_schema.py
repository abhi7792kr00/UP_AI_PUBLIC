from datetime import datetime

from pydantic import BaseModel


class OfficerComplaintItem(BaseModel):
    complaint_number: str
    subject: str
    description: str

    category_id: int
    priority_id: int
    status_id: int

    address: str | None = None

    assigned_at: datetime | None = None
    remarks: str | None = None


class OfficerDashboardResponse(BaseModel):
    officer_id: int
    officer_name: str
    employee_code: str

    total_assigned: int

    pending: int
    assigned: int
    in_progress: int
    resolved: int
    escalated: int
    reopened: int
    closed: int
    rejected: int

    complaints: list[OfficerComplaintItem] = []

    model_config = {
        "from_attributes": True,
    }