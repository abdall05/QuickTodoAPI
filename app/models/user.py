from pydantic import field_validator
from sqlmodel import Field ,SQLModel

from enum import Enum

class Role(str, Enum):
    USER = "user"
    ADMIN = "admin"


class UserBase(SQLModel):
    username: str = Field(min_length=3, max_length=20)
    name: str = Field(min_length=2, max_length=50)


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=64)
    password_confirm: str = Field(min_length=8, max_length=64)
    @field_validator("password_confirm")
    def passwords_match(cls, v, values):
        if "password" in values.data and v != values.data["password"]:
            raise ValueError("Passwords do not match")
        return v

class User(UserBase,table=True):
    id: int | None = Field(default=None, primary_key=True)
    password_hash: str
    role: Role = Field(default=Role.USER)


class UserPublic(UserBase):
    id: int
    role: Role = Field(default=Role.USER)

class UserLogin(SQLModel):
    username: str
    password: str

class UserWithToken(UserPublic):
    access_token: str
    token_type: str = "bearer"
