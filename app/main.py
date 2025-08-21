from dotenv import load_dotenv
from pathlib import Path

# load .env immediately at startup
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

from fastapi import FastAPI
from contextlib import asynccontextmanager
from.routers import auth
from .db import init_db



@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(auth.router)
