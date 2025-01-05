#app/models/funcionario.py
from datetime import datetime
import pytz
from sqlalchemy import (
    JSON,
    Boolean,
    DateTime,
    Integer,
    String,
    ForeignKey,
    Table,
    Column,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.config import settings
from typing import Optional, List


class Funcionario(settings.Base):
    __tablename__ = "funcionarios"
    __table_args__ = {"extend_existing": True}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    cargo: Mapped[str] = mapped_column(String(100), nullable=False)

    # Relacionamento com Produto
    itens_recebimento: Mapped["ItensRecebimento"] = relationship(
        "ItensRecebimento",
        back_populates="funcionario",
        lazy="joined",
    )
    
    def __repr__(self):
        return f"<Funcionario id={self.id} nome={self.nome}>"
