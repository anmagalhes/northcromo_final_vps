# app/controllers/ordem_controller.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import ordem_producao, Tarefa
from pydantic import BaseModel

router = APIRouter()

class ordem_producaoCreate(BaseModel):
    numero: str
    descricao: str
    data_criacao: str
    recebimento: str


@router.post("/ordens_producao/")
def create_ordem(ordem: ordem_producaoCreate, db: Session = Depends(get_db)):
    db_ordem = ordem_producao(**ordem.dict())
    db.add(db_ordem)
    db.commit()
    db.refresh(db_ordem)
    return db_ordem
