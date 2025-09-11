from app.models.user import User
from app.repositories.user import UserRepository


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def get_users(self):
        return self.repo.get_users()

    def get_user(self, user_id):
        return self.repo.get_user_by_id(user_id)

    def delete_user(self, user: User):
        self.repo.delete_user(user)
