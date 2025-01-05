# app/models/recebimento/recebimento.py
from datetime import datetime
import pytz
from sqlalchemy import (
    Integer,
    String,
    ForeignKey,
    DateTime,
    Boolean,

)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.config import settings
from typing import Optional, List

# Criando um timezone para São Paulo (UTC-3)
SP_TZ = pytz.timezone("America/Sao_Paulo")


# Função auxiliar para garantir o uso correto do timezone
def get_current_time_in_sp() -> datetime:
    return datetime.now(SP_TZ).astimezone(
        SP_TZ
    )  # Garante que a data e hora sejam "aware"


class Recebimento(settings.Base):
    __tablename__ = "recebimentos"
    __table_args__ = {"extend_existing": True}

    # Campos básicos
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tipo_ordem: Mapped[str] = mapped_column(String(20), nullable=False)
    recebimento_ordem: Mapped[int] = mapped_column(String(12), unique=False, nullable=False)
    
    # Campos de data e hora
    data_rec_ordem: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=get_current_time_in_sp)
    hora_inicial_ordem: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    data_final_ordem: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    hora_final_ordem: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)

    # Relacionamento com Produto (muitos para muitos)
    produtos: Mapped[List["Produto"]] = relationship(
        "Produto",  # Nome da classe relacionada
        secondary="itens_recebimento",  # Tabela intermediária para o relacionamento muitos-para-muitos
        back_populates="recebimentos",
    )

     # Relacionamento com ItensRecebimento
    itens: Mapped[List["ItensRecebimento"]] = relationship(
        "ItensRecebimento",
        back_populates="recebimento",
    )

    # Colunas de controle de data
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=get_current_time_in_sp
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=get_current_time_in_sp,
        onupdate=get_current_time_in_sp,
    )
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # Relacionamento com o modelo User (usando tipagem de string)
    usuario_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("usuario.id"), nullable=True
    )  # Tabela Campo

    # Relacionamento MANY-TO-ONE de Grupo_Produto para User (não 'Usuario')
    usuario: Mapped["User"] = relationship(
        "User",  # Referência correta à classe 'User'
        back_populates="recebimentos",  # Nome do campo de volta no User
        lazy="joined",
    )

    def __repr__(self):
        return f"<Recebimento id={self.id} tipo_ordem={self.tipo_ordem or 'Unnamed'} recebimento_ordem={self.recebimento_ordem or 'Unnamed'}>"