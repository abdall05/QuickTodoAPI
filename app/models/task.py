from datetime import datetime, timezone
from typing import Annotated
from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class TaskBase(SQLModel):
    title: str
    description: str | None = None


class Task(TaskBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class TaskCreate(TaskBase):
    pass


class TaskUpdate(SQLModel):
    title: str | None = None
    description: str | None = None
    completed: bool | None = None


class TaskPublic(TaskBase):
    id: int
    completed: bool
    created_at: datetime
