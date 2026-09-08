from enum import Enum


class AddressType(str, Enum):
    """
    Complaint Address Type
    """

    RURAL = "RURAL"

    URBAN = "URBAN"