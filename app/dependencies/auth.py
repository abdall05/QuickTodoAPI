from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from typing import Annotated
import jwt
from app.dependencies.user import get_user_repository
from app.models.auth import TokenData
from app.models.user import Role
from app.repositories.user import UserRepository
from app.services.auth import AuthService

from app.core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")  # tokenUrl here is just for docs, not used in code


def get_current_user(token: str = Depends(oauth2_scheme)) -> TokenData:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return TokenData(**payload)
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )


CurrentUserDep = Annotated[TokenData, Depends(get_current_user)]


def require_admin_user(user_token_data: TokenData = Depends(get_current_user)) -> TokenData:
    if user_token_data.role != Role.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource",
        )
    return user_token_data


AdminUserDependency = Annotated[TokenData, Depends(require_admin_user)]


def get_auth_service(
        repo: UserRepository = Depends(get_user_repository)
) -> AuthService:
    return AuthService(repo)


AuthServiceDependency = Annotated[AuthService, Depends(get_auth_service)]
