from __future__ import annotations
from datetime import datetime
from sqlalchemy import Integer, String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship  # Importando relationship

from app.utils.datetime import utcnow
from app.api.models.mixins import TimestampMixin
from app.api.models.base import Base
from app.api.models.produto import Produto  # Importando Produto, já que é necessário para o relacionamento

class Posto_Trabalho(Base, TimestampMixin):
    __tablename__ = "posto_trabalhos"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="Identificador único da operação"
    )

    posto_trabalho_nome: Mapped[str] = mapped_column(
        String(50),
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

    # Relacionamento com o modelo Produto
    produtos: Mapped[list[Produto]] = relationship(
        "Produto",
        back_populates="posto_trabalho"
    )
