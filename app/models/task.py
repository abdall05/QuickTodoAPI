from typing import Annotated
from pydantic import BaseModel
from sqlmodel import Field ,SQLModel



class TaskBase(SQLModel):
    title: str
    description: str | None = None
    completed: bool | None = False
class Task(SQLModel,table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int | None =  Field(default=None, foreign_key="user.id")

