import os
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import HTTPException
from sqlmodel import Session
from starlette import status

from ..crud.user import create_user,get_user_by_username
from ..models.user import UserCreate,UserWithToken,UserLogin,User,UserPublic

from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


#JWT
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM= os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def tokenize_user(user:User)->UserWithToken:
    payload = {"id": user.id, "role": user.role}
    access_token = create_access_token(payload)
    user_dict = user.model_dump()
    user_dict["access_token"] = access_token
    user_dict["token_type"] = "bearer"
    return UserWithToken(**user_dict)


def signup(user_create: UserCreate,session:Session) -> UserWithToken:
    hashed_password = get_password_hash(user_create.password)
    db_user = User(**user_create.model_dump(), password_hash=hashed_password)
    db_user=create_user(db_user,session)
    return tokenize_user(db_user)


def signin(user: UserLogin,session:Session) -> UserWithToken:
    db_user = get_user_by_username(user.username,session)
    if db_user is None or not verify_password(user.password,db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return tokenize_user(db_user)

