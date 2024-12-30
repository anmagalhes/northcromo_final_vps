# app/controllers/tarefa_controller.py

from core.desp import get_session
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tarefa import Tarefa

router = APIRouter(prefix="/todos", tags=["tarefa"])


class TarefaCreate(BaseModel):
    nome: str
    descricao: str
    ordem_producao_id: int


@router.post("/tarefas/")
def create_tarefa(tarefa: TarefaCreate, db: AsyncSession = Depends(get_session)):
    db_tarefa = Tarefa(**tarefa.dict())
    db.add(db_tarefa)
    db.commit()
    db.refresh(db_tarefa)
    return db_tarefa
