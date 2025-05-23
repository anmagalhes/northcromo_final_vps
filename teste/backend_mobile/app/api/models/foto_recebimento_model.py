#app/api/models/foto_recebimento_model.py

from __future__ import annotations
from datetime import datetime
from typing import Optional

from sqlalchemy import Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.base_class import Base


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.api.models.recebimento import Recebimento


class FotoRecebimento(Base):
    __tablename__ = "foto_recebimento"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_ordem: Mapped[int] = mapped_column(ForeignKey('recebimentos.id'), nullable=False, index=True)
    nome_foto: Mapped[str] = mapped_column(String(255), nullable=False)

    recebimento = relationship("Recebimento", back_populates="fotos")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    def __repr__(self) -> str:
        return f"<FotoRecebimento ordem_id={self.id_ordem} nome={self.nome_foto}>"
