from collections.abc import Generator
from sqlmodel import SQLModel, create_engine, Session
from config import cfg
from typing import Annotated
from fastapi import Depends


sqliteEngine = create_engine(cfg.SQLITE_URI)


def init_db():
    SQLModel.metadata.create_all(sqliteEngine)


def get_db() -> Generator[Session, None, None]:
    with Session(sqliteEngine) as session:
        yield session


SqliteDBDep = Annotated[Session, Depends(get_db)]
