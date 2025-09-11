from sqlmodel import Session, select, delete
from app.models.task import Task


class TaskRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_task_by_id(self, task_id: int) -> Task | None:
        task = self.session.exec(select(Task).where(Task.id == task_id)).first()
        return task

    def get_user_tasks(self, user_id: int) -> list[Task]:
        statement = select(Task).where(Task.user_id == user_id)
        return list(self.session.exec(statement).all())

    def save_task(self, task: Task) -> Task:
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def create_task(self, task: Task) -> Task:
        return self.save_task(task)

    def delete_task(self, task: Task):
        self.session.delete(task)
        self.session.commit()

    def delete_tasks(self, user_id: int):
        statement = delete(Task).where(Task.user_id == user_id)
        self.session.exec(statement)  # type: ignore
        self.session.commit()

    def update_task(self, updated_task) -> Task:
        return self.save_task(updated_task)
