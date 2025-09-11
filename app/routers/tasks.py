from fastapi import APIRouter, status, HTTPException
from fastapi.responses import Response

from app.dependencies.auth import CurrentUserDep
from app.dependencies.task import TaskServiceDependency
from app.models.task import TaskPublic, TaskCreate, TaskUpdate, Task
from app.services.task import TaskService

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)


def get_task_or_404(service: TaskService, task_id: int, user_id: int) -> Task:
    task = service.get_task_by_id(task_id, user_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


@router.get("/{task_id}", response_model=TaskPublic)
async def get_task(task_id: int, current_user: CurrentUserDep, service: TaskServiceDependency):
    return get_task_or_404(service, task_id, current_user.id)


@router.get("/", response_model=list[TaskPublic])
async def get_tasks(current_user: CurrentUserDep, service: TaskServiceDependency):
    user_id = current_user.id
    tasks = service.get_tasks(user_id)
    return tasks


@router.post("/", response_model=TaskPublic)
async def create_task(task: TaskCreate, current_user: CurrentUserDep, service: TaskServiceDependency):
    user_id = current_user.id
    db_task = service.create_task(task, user_id)
    return db_task


@router.delete("/{task_id}")
async def delete_task(task_id: int, current_user: CurrentUserDep, service: TaskServiceDependency):
    task = get_task_or_404(service, task_id, current_user.id)
    service.delete_task(task)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/")
async def delete_tasks(current_user: CurrentUserDep, service: TaskServiceDependency):
    user_id = current_user.id
    service.delete_tasks(user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch("/{task_id}")
async def update_task(task_id: int, task_data: TaskUpdate, current_user: CurrentUserDep,
                      service: TaskServiceDependency) -> TaskPublic:
    task = get_task_or_404(service, task_id, current_user.id)
    updated_task = service.update_task(task, task_data)
    return updated_task
