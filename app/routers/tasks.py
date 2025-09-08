from fastapi import APIRouter, status
from fastapi.responses import Response

from ..dependencies.auth import CurrentUserDep
from ..dependencies.db import SessionDep
from ..models.task import TaskPublic, TaskCreate, TaskUpdate
from ..services import task as TaskService

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)


@router.get("/")
async def get_tasks(current_user: CurrentUserDep, session: SessionDep) -> list[TaskPublic]:
    user_id = current_user.id
    tasks = TaskService.get_tasks(user_id, session)
    return list(tasks)


@router.post("/")
async def create_task(task: TaskCreate, current_user: CurrentUserDep, session: SessionDep) -> TaskPublic:
    user_id = current_user.id
    db_task = TaskService.create_task(task, user_id, session)
    task_public = TaskPublic(**db_task.model_dump())
    return task_public


@router.delete("/{task_id}")
async def delete_task(task_id: int, current_user: CurrentUserDep, session: SessionDep):
    user_id = current_user.id
    TaskService.delete_task(task_id, user_id, session)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/")
async def delete_task(current_user: CurrentUserDep, session: SessionDep):
    user_id = current_user.id
    TaskService.delete_tasks(user_id, session)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch("/{task_id}")
async def update_task(task_id: int, task_data: TaskUpdate, current_user: CurrentUserDep,
                      session: SessionDep) -> TaskPublic:
    user_id = current_user.id
    updated_task = TaskService.update_task(task_id, task_data, user_id, session)
    return updated_task
