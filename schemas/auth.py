
from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    full_name: str = Field(
        min_length=2,
        max_length=150
    )

    email: EmailStr

    phone: str = Field(
        min_length=10,
        max_length=20
    )

    password: str = Field(
        min_length=8,
        max_length=128
    )