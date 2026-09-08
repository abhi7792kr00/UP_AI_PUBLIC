from enum import Enum


class ComplaintSource(str, Enum):
    """
    Complaint Source
    """

    WEB = "WEB"

    ANDROID = "ANDROID"

    IOS = "IOS"

    WHATSAPP = "WHATSAPP"

    CALL_CENTER = "CALL_CENTER"

    CSC = "CSC"

    OFFICE = "OFFICE"

    API = "API"