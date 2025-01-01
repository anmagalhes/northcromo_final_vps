# app/schemas/task_schema.py
from pydantic import BaseModel

from app.models.todo import TodoState


class TodoSchema(BaseModel):
    titulo: str
    descricao: str
    status: TodoState


class TodoPublic(TodoSchema):
    id: int


class TodoList(BaseModel):
    todos: list[TodoPublic]


class TodoUpdate(BaseModel):
    titulo: str | None = None
    descricao: str | None = None
    status: TodoState | None = None
