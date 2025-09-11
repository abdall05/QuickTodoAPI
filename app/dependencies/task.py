from typing import Annotated

from fastapi import Depends, HTTPException,status
from sqlmodel import Session

from app.dependencies.auth import CurrentUserDep
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


def get_task_or_404(
    task_id: int,
    current_user: CurrentUserDep,
    service: TaskServiceDependency
):
    task = service.get_task_by_id(task_id, current_user.id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task
