# app/controllers/task_controller.py
from core.desp import get_session
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schema.task_schema import (
    TaskSchema,  # Corrigido 'schema' para 'schemas'
)
from app.services import task_service

router = APIRouter()


@router.post("/orders/{order_id}/tasks/", response_model=TaskSchema)
def add_task(
    order_id: int, task: TaskSchema, db: AsyncSession = Depends(get_session)
):  # Corrigido para 'Depends(get_db)'
    return task_service.add_task_to_order(db=db, order_id=order_id, task=task)
