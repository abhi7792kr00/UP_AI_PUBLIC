from app.services.base.base_service import BaseService
from app.repositories.master.locality_repository import (
    locality_repository,
)


class LocalityService(
    BaseService
):
    def __init__(self):
        super().__init__(
            locality_repository
        )


locality_service = LocalityService()