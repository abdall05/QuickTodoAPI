# db.py
from sqlmodel import SQLModel, Session, create_engine
from .models.task import Task
from .models.user import User
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})

def get_session():
    with Session(engine) as session:
        yield session
def init_db():
    SQLModel.metadata.create_all(engine)
