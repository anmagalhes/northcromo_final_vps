from __future__ import annotations
from datetime import datetime
from sqlalchemy import Integer, String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.api.models.base import Base
from app.api.models.mixins import TimestampMixin

class Funcao(Base, TimestampMixin):
    __tablename__ = "funcoes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    funcao_nome: Mapped[str] = mapped_column(String(150), nullable=False, unique=True, comment="Nome da função/cargo")

    data_cadastro: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Relacionamento inverso para Funcionario
    funcionarios: Mapped[list["Funcionario"]] = relationship(
        "Funcionario",
        back_populates="funcao_rel",
        cascade="all, delete-orphan"
    )
