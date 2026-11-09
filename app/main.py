"""Run from the repository root with python -m uvicorn app.main:app."""
import os
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Annotated

from fastapi import FastAPI, status
from pydantic import BaseModel, StringConstraints

from app import database


class TaskInput(BaseModel):
    title: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=100)]


class Task(TaskInput):
    id: int


def create_app(db_path: Path | None = None) -> FastAPI:
    path = db_path if db_path is not None else Path(os.getenv("TASKFLOW_DB", "data/taskflow.db"))

    @asynccontextmanager
    async def lifespan(api: FastAPI):
        database.initialise(path)
        yield

    api = FastAPI(title="TaskFlow", version="0.1.0", lifespan=lifespan)

    @api.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "service": "taskflow"} 

    @api.get("/tasks", response_model=list[Task])
    def read_tasks():
        return database.list_tasks(path)

    @api.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
    def add_task(task: TaskInput):
        return database.create_task(path, task.title)

    return api


app = create_app()
