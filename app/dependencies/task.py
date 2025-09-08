from typing import Annotated

from fastapi import Depends
from sqlmodel import Session
from app.repositories.task import TaskRepository
from app.dependencies.db import get_session
from app.services.task import TaskService


def get_task_repository(session: Session = Depends(get_session)) -> TaskRepository:
    return TaskRepository(session)


def get_task_service(
        repo: TaskRepository = Depends(get_task_repository)
) -> TaskService:
    return TaskService(repo)


TaskServiceDependency = Annotated[TaskService, Depends(get_task_service)]
