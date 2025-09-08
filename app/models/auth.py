from sqlmodel import SQLModel, Field

from app.models.user import Role, UserPublic


class AccessToken(SQLModel):
    access_token: str
    token_type: str = Field(default="Bearer", const=True)


class TokenData(SQLModel):
    id: int
    role: Role = Field(default=Role.USER)


class AuthResponse(SQLModel):
    user: UserPublic
    token: AccessToken
