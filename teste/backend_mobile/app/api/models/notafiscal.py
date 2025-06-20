# app/models/notafiscal/nota_fiscal.py
from __future__ import annotations
from datetime import date
from typing import List

from sqlalchemy import String, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.api.models.mixins import TimestampMixin
from app.api.models.base import Base

class NotaFiscal(Base, TimestampMixin):
    __tablename__ = "notas_fiscais"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        comment="ID único da nota fiscal"
    )

    numero_nota_fiscal: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        unique=True,  # Garante que cada NF seja única
        comment="Número da nota fiscal",
        index=True
    )

    data_emissao: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        comment="Data de emissão"
    )

    # Relação 1:N com Recebimentos
    recebimentos: Mapped[List["Recebimento"]] = relationship(
        "Recebimento",
        back_populates="nota_fiscal"
    )

    def __repr__(self):
        return f"<NotaFiscal {self.numero} ({self.data_emissao})>"
