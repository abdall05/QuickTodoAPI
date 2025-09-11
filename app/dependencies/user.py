from typing import Annotated

from fastapi import Depends
from sqlmodel import Session
from app.repositories.user import UserRepository
from app.dependencies.db import get_session
from app.services.user import UserService


def get_user_repository(session: Session = Depends(get_session)) -> UserRepository:
    return UserRepository(session)


def get_user_service(repo: UserRepository = Depends(get_user_repository)) -> UserService:
    return UserService(repo)


UserServiceDependency = Annotated[UserService, Depends(get_user_service)]
