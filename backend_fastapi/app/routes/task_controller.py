# app/controllers/task_controller.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from sqlalchemy.orm import Session

from core.desp import get_session, get_current_user

from app.services import task_service
from app.schema.task_schema import TaskSchema  # Corrigido 'schema' para 'schemas'

router = APIRouter()

@router.post("/orders/{order_id}/tasks/", response_model=TaskSchema)
def add_task(order_id: int, task: TaskSchema, db: AsyncSession = Depends(get_session)):  # Corrigido para 'Depends(get_db)'
    return task_service.add_task_to_order(db=db, order_id=order_id, task=task)
