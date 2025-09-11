from sqlmodel import Session, select

from app.models.user import User


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_user(self, user: User) -> User:
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def get_user_by_id(self, user_id: int) -> User | None:
        return self.session.get(User, user_id)

    def get_user_by_username(self, username: str) -> User | None:
        statement = select(User).where(User.username == username)
        result = self.session.exec(statement).first()
        return result

    def delete_user(self, user: User) -> None:
        self.session.delete(user)
        self.session.commit()

    def get_users(self) -> list[User]:
        return list(self.session.exec(select(User)).all())

