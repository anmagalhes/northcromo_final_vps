from __future__ import annotations
from sqlalchemy import Integer, String, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.api.models.base import Base
from enum import Enum as PyEnum

class TipoGrupo(PyEnum):
    PRODUTO = "PRODUTO"
    SERVICO = "SERVIÇO"

class Grupo(Base):
    __tablename__ = "grupos"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="Identificador único do grupo"
    )

    grupo_nome: Mapped[TipoGrupo] = mapped_column(
        Enum(TipoGrupo),  # Aqui estamos dizendo que o campo grupo_nome é baseado no Enum TipoGrupo
        nullable=False,
        unique=True,
        comment="Nome do grupo"
    )

    # Relacionamento com Produto (um grupo pode conter muitos produtos)
    produtos: Mapped[list[Produto]] = relationship("Produto", back_populates="grupos")

    def __repr__(self):
        return f"<Grupo(id={self.id}, nome={self.grupo_nome})>"
