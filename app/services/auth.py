from datetime import datetime, timedelta, timezone
from app.core.config import settings
import jwt
from app.models.auth import AccessToken, TokenData, AuthResponse
from app.models.user import UserCreate, UserLogin, User, UserPublic
from passlib.context import CryptContext

from app.repositories.user import UserRepository

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def create_access_token(payload: TokenData) -> AccessToken:
        to_encode = payload.model_dump()
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return AccessToken(access_token=encoded_jwt)

    @staticmethod
    def tokenize_user(user: User) -> AuthResponse:
        payload = TokenData(id=user.id, role=user.role)
        access_token = AuthService.create_access_token(payload)
        user_public = UserPublic.model_validate(user)
        return AuthResponse(user=user_public, token=access_token)

    def login(self, user: UserLogin) -> AuthResponse | None:
        db_user = self.repo.get_user_by_username(user.username)
        if db_user is None or not self.verify_password(user.password, db_user.password_hash):
            return None
        return AuthService.tokenize_user(db_user)

    def signup(self, user_create: UserCreate) -> AuthResponse:
        hashed_password = AuthService.hash_password(user_create.password)
        extra_data = {"hashed_password": hashed_password}
        db_user = User.model_validate(user_create, update=extra_data)
        db_user = self.repo.create_user(db_user)
        return AuthService.tokenize_user(db_user)
