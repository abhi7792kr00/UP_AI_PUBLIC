from app.dto.common.base import BaseDTO


class PaginationDTO(BaseDTO):
    """
    Pagination information.
    """

    page: int = 1

    page_size: int = 10

    total_items: int = 0

    total_pages: int = 0