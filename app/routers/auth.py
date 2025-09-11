from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.dependencies.auth import AuthServiceDependency
from app.exceptions import UserAlreadyExists
from app.models.auth import AccessToken
from app.models.user import UserCreate, UserLogin

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("/signup")
async def signup(*, user: UserCreate, service: AuthServiceDependency) -> AccessToken:
    try:
        new_user = service.signup(user)
        return new_user
    except UserAlreadyExists as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
async def login(*, form_data: OAuth2PasswordRequestForm = Depends(), service: AuthServiceDependency) -> AccessToken:
    user_login = UserLogin(username=form_data.username, password=form_data.password)
    auth_response = service.login(user_login)
    if auth_response is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return auth_response
