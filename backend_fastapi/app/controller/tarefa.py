# app/controllers/tarefa_controller.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.tarefa import Tarefa
from pydantic import BaseModel

router = APIRouter()


class TarefaCreate(BaseModel):
    nome: str
    descricao: str
    ordem_producao_id: int


@router.post("/tarefas/")
def create_tarefa(tarefa: TarefaCreate, db: Session = Depends(get_db)):
    db_tarefa = Tarefa(**tarefa.dict())
    db.add(db_tarefa)
    db.commit()
    db.refresh(db_tarefa)
    return db_tarefa
