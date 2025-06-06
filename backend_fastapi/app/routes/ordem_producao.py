# app/controllers/ordem_controller.py
from core.desp import get_session
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import ordem_producao

router = APIRouter()


class ordem_producaoCreate(BaseModel):
    numero: str
    descricao: str
    data_criacao: str
    recebimento: str


@router.post("/ordens_producao/")
def create_ordem(ordem: ordem_producaoCreate, db: AsyncSession = Depends(get_session)):
    db_ordem = ordem_producao(**ordem.dict())
    db.add(db_ordem)
    db.commit()
    db.refresh(db_ordem)
    return db_ordem
