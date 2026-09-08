from pydantic import BaseModel


class DashboardResponse(BaseModel):
    total_officers: int

    active_postings: int

    total_transfers: int

    total_promotions: int

    total_leaves: int

    active_suspensions: int

    total_retirements: int

    completed_trainings: int

    model_config = {
        "from_attributes": True,
    }