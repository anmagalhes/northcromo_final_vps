# app/schemas/task_schema.py
from pydantic import BaseModel
from typing import List, Optional


class TaskSchema(BaseModel):
    title: str
    description: Optional[str] = None
    status: str = "Pending"

    class Config:
        from_attributes = True
