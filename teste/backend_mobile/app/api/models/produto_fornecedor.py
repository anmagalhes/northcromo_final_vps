# app/api/models/produto_fornecedor.py
from __future__ import annotations
from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Index

from app.api.models.base import Base

class ProdutoFornecedor(Base):
    __tablename__ = "produto_fornecedor"

    produto_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("produtos.id", ondelete="CASCADE"),
        primary_key=True,
        comment="ID do produto"
    )

    fornecedor_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("fornecedores.id", ondelete="CASCADE"),
        primary_key=True,
        comment="ID do fornecedor"
    )

     # Adicionando índices para otimizar a busca
    __table_args__ = (
        Index('ix_produto_id', 'produto_id'),  # Índice para produto_id
        Index('ix_fornecedor_id', 'fornecedor_id'),  # Índice para fornecedor_id
    )
