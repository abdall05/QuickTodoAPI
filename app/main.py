from app.core.config import settings
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routers.auth import router as auth_router
from app.routers.tasks import router as task_router
from app.routers.users import router as user_router

from app.db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)
app.include_router(task_router)
app.include_router(user_router)
