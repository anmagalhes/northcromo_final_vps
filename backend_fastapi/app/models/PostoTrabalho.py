# app/models/componente.py
from datetime import datetime
import pytz
from sqlalchemy import (
    Integer,
    String,
    ForeignKey,
    DateTime,
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


class Postotrabalho(settings.Base):
    __tablename__ = "Postotrabalho_novos"
    __table_args__ = {"extend_existing": True}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(40), unique=True, nullable=False)

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
        back_populates="Postotrabalhos",  # Nome do campo de volta no User
        lazy="joined",
    )

    # Relacionamento com Produto
    produtos: Mapped[List["Produto"]] = relationship(
        "Produto",  # Nome da classe de destino
        back_populates="Postotrabalhos",  # Nome do campo de volta em Operacao
        lazy="joined",  # Carregamento desejado
        uselist=True  # Isso permite que seja uma lista de objetos Operacao
    )

    def __repr__(self):
        return (
            f'<Postotrabalho id={self.id} name={self.name if self.name else "Unnamed"}>'
        )