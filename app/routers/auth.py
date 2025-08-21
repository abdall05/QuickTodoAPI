from fastapi import APIRouter
from ..models.user import UserCreate,UserWithToken,UserLogin
from ..services import auth
from ..dependencies.db import SessionDep
router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("/signup")
async def signup(user: UserCreate,session:SessionDep)->UserWithToken:
    return auth.signup(user,session)

@router.post("/login")
async def login(user: UserLogin,session:SessionDep)->UserWithToken:
    return auth.signin(user,session)
