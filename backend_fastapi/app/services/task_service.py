# app/services/task_service.py
from app.models.task import Task
from app.schema.task_schema import TaskSchema
from sqlalchemy.orm import Session
from typing import List


def add_task_to_order(db: Session, order_id: int, task: TaskSchema) -> Task:
    db_task = Task(title=task.title, description=task.description, order_id=order_id, status=task.status)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task
