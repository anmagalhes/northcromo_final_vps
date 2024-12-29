# app/schemas/order_schema.py
from pydantic import BaseModel
from typing import List, Optional
from schema.task_schema import TaskSchema


class OrderSchema(BaseModel):
    title: str
    description: Optional[str] = None
    tasks: List[TaskSchema] = []

    class Config:
        orm_mode = True
