# app/schemas/order_schema.py
from typing import List, Optional

from pydantic import BaseModel

from schema.task_schema import TaskSchema


class OrderSchema(BaseModel):
    title: str
    description: Optional[str] = None
    tasks: List[TaskSchema] = []

    class Config:
        from_attributes = True
