from fastapi import APIRouter, status, HTTPException
from fastapi.responses import Response

from app.dependencies.auth import CurrentUserDep, AdminUserDependency
from app.dependencies.user import UserServiceDependency
from app.models.user import User, UserPublic

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.get("/", response_model=list[User])
async def get_users(current_admin: AdminUserDependency, service: UserServiceDependency):
    return service.get_users()


@router.get("/me", response_model=UserPublic)
async def get_me(current_user: CurrentUserDep, service: UserServiceDependency):
    return service.get_user(current_user.id)


@router.get("/{user_id}", response_model=User)
async def get_user(user_id: int, current_admin: AdminUserDependency, service: UserServiceDependency):
    return service.get_user(user_id)


@router.delete("/{user_id}")
async def delete_user(user_id: int, current_admin: AdminUserDependency, service: UserServiceDependency):
    if current_admin.id == user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You cannot delete your own account."
        )
    user = service.get_user(user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    service.delete_user(user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
