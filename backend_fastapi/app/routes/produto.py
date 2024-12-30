# app/controllers/produto_controller.py
from core.desp import get_session
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

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
