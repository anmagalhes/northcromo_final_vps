from __future__ import annotations
from datetime import datetime
from sqlalchemy import Integer, String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from app.utils.datetime import utcnow
from app.api.models.mixins import TimestampMixin
from app.api.models.base import Base

class Operacao(Base, TimestampMixin):
    __tablename__ = "operacoes"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="Identificador único da operação"
    )

    op_grupo_processo: Mapped[str] = mapped_column(
        String(3),
        nullable=False,
        comment="Grupo de processo da operação"
    )

    op_nome: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        comment="Nome da operação"
    )

    data_execucao: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utcnow,
        nullable=False,
        server_default=func.now(),
        comment="Data e hora do registro do componente"
    )
