from app.models.task import Task, TaskCreate, TaskUpdate
from app.repositories.task import TaskRepository


class TaskService:
    def __init__(self, repo: TaskRepository):
        self.repo = repo

    def get_tasks(self, user_id: int) -> list[Task]:
        return self.repo.get_user_tasks(user_id)

    def get_task_by_id(self, task_id: int, user_id: int) -> Task | None:
        task = self.repo.get_task_by_id(task_id)
        if not task or (task.user_id != user_id):
            return None
        return task

    def create_task(self, task_data: TaskCreate, user_id: int) -> Task:
        task = Task.model_validate(task_data, update={'user_id': user_id})
        db_task = self.repo.create_task(task)
        return db_task

    def update_task(self, task: Task, task_update_data: TaskUpdate) -> Task | None:
        update_data = task_update_data.model_dump(exclude_unset=True)
        task.sqlmodel_update(update_data)
        return self.repo.save_task(task)

    def delete_task(self, task: Task) -> None:
        self.repo.delete_task(task)

    def delete_tasks(self, user_id: int) -> None:
        self.repo.delete_tasks(user_id)
