from datetime import datetime
import pytz
from sqlalchemy import (
    Enum,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Boolean,
    Text,
    Date,
    Float,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.config import settings
from typing import Optional, List
import enum


# Criando um timezone para São Paulo (UTC-3)
SP_TZ = pytz.timezone("America/Sao_Paulo")


# Função auxiliar para garantir o uso correto do timezone
def get_current_time_in_sp() -> datetime:
    return datetime.now(SP_TZ).astimezone(
        SP_TZ
    )  # Garante que a data e hora sejam "aware"


class FotoRecebimento(settings.Base):
    __tablename__ = "fotos_recebimento"
    __table_args__ = {"extend_existing": True}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    url_foto: Mapped[str | None] = mapped_column(Text, nullable=True)

    item_recebimento_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("itens_recebimento.id"), nullable=False
    )

    # Relacionamento
    item_recebimento = relationship("ItensRecebimento", back_populates="fotos")
