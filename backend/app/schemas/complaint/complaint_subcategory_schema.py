from pydantic import BaseModel
from pydantic import ConfigDict


class ComplaintSubCategoryBase(
    BaseModel,
):
    category_id: int

    subcategory_name: str

    subcategory_code: str

    description: str | None = None


class ComplaintSubCategoryCreate(
    ComplaintSubCategoryBase,
):
    pass


class ComplaintSubCategoryUpdate(
    BaseModel,
):
    category_id: int | None = None

    subcategory_name: str | None = None

    subcategory_code: str | None = None

    description: str | None = None


class ComplaintSubCategoryResponse(
    ComplaintSubCategoryBase,
):
    id: int

    model_config = ConfigDict(
        from_attributes=True,
    )