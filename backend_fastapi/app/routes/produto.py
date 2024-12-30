# app/controllers/produto_controller.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from sqlalchemy.orm import Session

from core.desp import get_session, get_current_user

from app.models import produto
from pydantic import BaseModel

router = APIRouter()


class ProdutoCreate(BaseModel):
    nome: str
    descricao: str
    grupo_produto_id: int


@router.post("/produtos/")
def create_produto(produto: ProdutoCreate, db: AsyncSession = Depends(get_session)):
    db_produto = produto(**produto.dict())
    db.add(db_produto)
    db.commit()
    db.refresh(db_produto)
    return db_produto
