# app/schemas/task_schema.py
from typing import Optional

from pydantic import BaseModel


class TaskSchema(BaseModel):
    title: str
    description: Optional[str] = None
    status: str = "Pending"

    class Config:
        from_attributes = True
