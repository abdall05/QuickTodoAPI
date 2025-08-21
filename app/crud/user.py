from sqlmodel import select,Session

from app.models.user import User


def create_user(user:User,session:Session):
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
def get_user_by_username(username: str, session: Session) -> User | None:
    statement = select(User).where(User.username == username)
    result = session.exec(statement).first()
    return result