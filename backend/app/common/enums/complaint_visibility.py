from enum import Enum


class ComplaintVisibility(str, Enum):
    """
    Complaint Visibility
    """

    PUBLIC = "PUBLIC"

    PRIVATE = "PRIVATE"