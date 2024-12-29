# app/controllers/produto_controller.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import produto, grupo_produto
from pydantic import BaseModel

router = APIRouter()

class ProdutoCreate(BaseModel):
    nome: str
    descricao: str
    grupo_produto_id: int


@router.post("/produtos/")
def create_produto(produto: ProdutoCreate, db: Session = Depends(get_db)):
    db_produto = produto(**produto.dict())
    db.add(db_produto)
    db.commit()
    db.refresh(db_produto)
    return db_produto
