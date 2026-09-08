from pydantic import BaseModel


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