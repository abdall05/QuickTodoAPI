from fastapi import APIRouter, status
from fastapi.responses import Response

from ..dependencies.auth import CurrentUserDep
from ..dependencies.db import SessionDep
from ..dependencies.task import TaskServiceDependency
from ..models.task import TaskPublic, TaskCreate, TaskUpdate

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)


@router.get("/")
async def get_tasks(current_user: CurrentUserDep, service: TaskServiceDependency) -> list[TaskPublic]:
    user_id = current_user.id
    tasks = service.get_tasks(user_id)
    return tasks


@router.post("/",response_model=TaskPublic)
async def create_task(task: TaskCreate, current_user: CurrentUserDep, service: TaskServiceDependency):
    user_id = current_user.id
    db_task = service.create_task(task, user_id)
    return db_task


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
