from fastapi import Depends
from sqlmodel import Session
from app.repositories.user import UserRepository
from app.dependencies.db import get_session


def get_user_repository(session: Session = Depends(get_session)) -> UserRepository:
    return UserRepository(session)
