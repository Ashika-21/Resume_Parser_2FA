
from pydantic import BaseModel, ConfigDict, Field, EmailStr


class ProfileUpdate(BaseModel):
    full_name: str | None = Field(default=None, min_length=2)
    email: EmailStr | None = None
    phone: str | None = None


class ProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: str
    email: str
    phone: str
    is_active: bool