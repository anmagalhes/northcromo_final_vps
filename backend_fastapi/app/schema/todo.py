# app/schemas/task_schema.py
from pydantic import BaseModel
from typing import List, Optional
from app.models.todo import TodoState

class TodoSchema(BaseModel):
    titulo: str
    descricao: str
    status: TodoState


class TodoPublic(TodoSchema):
    id: int