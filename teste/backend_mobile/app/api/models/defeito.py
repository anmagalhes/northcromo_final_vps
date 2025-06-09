# app/api/models/defeito.py
from __future__ import annotations
from datetime import datetime
from sqlalchemy import Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.utils.datetime import utcnow
from app.api.models.mixins import TimestampMixin
from app.api.models.base import Base

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.api.models.componente import Componente


class Defeito(Base, TimestampMixin):
    __tablename__ = "defeitos"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="Identificador único do defeito"
    )

    data: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utcnow,
        nullable=False,
        server_default=func.now(),
        comment="Data e hora do registro do defeito"
    )

    componente_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("componentes.id", ondelete="CASCADE"),
        nullable=False,
        comment="ID do componente associado"
    )

    def_nome: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        comment="Nome do defeito"
    )

    # Relacionamento com Component
    componente: Mapped[Componente] = relationship("Componente", back_populates="defeitos")
