from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import ConfigDict


class UserBase(BaseModel):

    full_name: str

    username: str

    email: EmailStr

    mobile: str | None = None

    role_id: int


class UserCreate(UserBase):

    password: str

    officer_id: int | None = None


class UserUpdate(BaseModel):

    full_name: str

    email: EmailStr

    mobile: str | None = None

    role_id: int

    officer_id: int | None = None

    is_active: bool


class UserResponse(UserBase):

    id: int

    is_active: bool

    officer_id: int | None = None

    model_config = ConfigDict(
        from_attributes=True,
    )