# app/api/models/componente.py

from __future__ import annotations
from datetime import datetime
from sqlalchemy import Integer, String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column,  relationship

from app.utils.datetime import utcnow
from app.api.models.mixins import TimestampMixin
from app.api.models.base import Base
from typing import List

class Componente(Base, TimestampMixin):
    __tablename__ = "componentes"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="Identificador único do componente"
    )

    componente_nome: Mapped[str] = mapped_column(
        String(25),
        nullable=False,
        comment="Nome do componente"
    )

    data_recebimento: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utcnow,
        nullable=False,
        server_default=func.now(),
        comment="Data e hora do registro do componente"
    )

    defeitos: Mapped[List[Defeito]] = relationship("Defeito", back_populates="componente")
