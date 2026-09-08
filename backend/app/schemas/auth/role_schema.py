from pydantic import BaseModel, ConfigDict


class RoleBase(BaseModel):
    role_name: str
    description: str | None = None


class RoleCreate(RoleBase):
    pass


class RoleUpdate(RoleBase):
    pass


class RoleResponse(RoleBase):
    id: int
    is_active: bool

    model_config = ConfigDict(
        from_attributes=True
    )