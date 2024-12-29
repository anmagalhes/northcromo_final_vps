# app/controllers/task_controller.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services import task_service
from app.schema.task_schema import TaskSchema  # Corrigido 'schema' para 'schemas'
from app.database import SessionLocal  # Certifique-se de que 'SessionLocal' está configurado corretamente
from app.database import get_db  # Importando a função 'get_db', que é necessária

router = APIRouter()

@router.post("/orders/{order_id}/tasks/", response_model=TaskSchema)
def add_task(order_id: int, task: TaskSchema, db: Session = Depends(get_db)):  # Corrigido para 'Depends(get_db)'
    return task_service.add_task_to_order(db=db, order_id=order_id, task=task)
