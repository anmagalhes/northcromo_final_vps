# app/api/models/produto.py
from __future__ import annotations
from datetime import datetime
from sqlalchemy import Integer, String, DateTime, ForeignKey, Enum as SAEnum, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from enum import Enum as PyEnum

from app.utils.datetime import utcnow
from app.api.models.mixins import TimestampMixin
from app.api.models.base import Base

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.api.models.componente import Componente
    from app.api.models.operacao import Operacao
    from app.api.models.posto_trabalho import Posto_Trabalho
    from app.api.models.fornecedor import Fornecedor

# Enum para o tipo de grupo (definido com o PyEnum do Python)
class TipoGrupo(PyEnum):
    PRODUTO = "PRODUTO"
    SERVICO = "SERVICO"

class Produto(Base, TimestampMixin):
    __tablename__ = "produtos"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="Identificador único do produto"
    )

    cod_produto: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        unique=True,
        comment="Código único do produto"
    )

    produto_nome: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="Nome do produto"
    )

    componente_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("componentes.id", ondelete="CASCADE"),
        nullable=False,
        comment="ID do componente associado"
    )

    operacao_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("operacoes.id", ondelete="CASCADE"),
        nullable=False,
        comment="ID da operação associada"
    )

    und_servicos: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment="Unidade de serviço do produto"
    )

    # Usando Enum do SQLAlchemy para definir se é PRODUTO ou SERVIÇO
    grupo_id: Mapped[TipoGrupo] = mapped_column(
        SAEnum(TipoGrupo),
        nullable=False,
        comment="Tipo de grupo: PRODUTO ou SERVIÇO"
    )

    tipo_produto: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        comment="1 - Produto, 2 - Tarefa"
    )

     # ✅ Adiciona campo `data` com valor automático
    data: Mapped[datetime] = mapped_column(
    DateTime(timezone=True),
    nullable=False,
    comment="Data de criação do produto",
    server_default=func.now()  # usado só se o frontend NÃO enviar
)

    posto_trabalho_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("posto_trabalhos.id", ondelete="CASCADE"),
        nullable=False,
        comment="ID do posto de trabalho associado"
    )

    # Relacionamento muitos para muitos com Fornecedores via tabela intermediária
    fornecedores: Mapped[list[Fornecedor]] = relationship(
        "Fornecedor",
        secondary="produto_fornecedor",  # Tabela intermediária
        back_populates="produtos",
        lazy="selectin"
    )

    # Relacionamentos
    componente: Mapped[Componente] = relationship("Componente", back_populates="produtos", lazy="joined")
    operacao: Mapped[Operacao] = relationship("Operacao", back_populates="produtos", lazy="joined")
    posto_trabalho: Mapped[Posto_Trabalho] = relationship("Posto_Trabalho", back_populates="produtos", lazy="joined")

    def __repr__(self):
        return f"<Produto(id={self.id}, cod_produto={self.cod_produto}, nome={self.produto_nome})>"
