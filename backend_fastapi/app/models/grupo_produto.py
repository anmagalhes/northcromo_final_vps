# app/models/grupo_produto.py
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

# Criando um timezone para São Paulo (UTC-3)
SP_TZ = pytz.timezone("America/Sao_Paulo")

# Função auxiliar para garantir o uso correto do timezone
def get_current_time_in_sp() -> datetime:
    return datetime.now(SP_TZ).astimezone(
        SP_TZ
    )  # Garante que a data e hora sejam "aware"


# TESTE


# Alternativa: utilizar UTC
def get_current_time_in_utc() -> datetime:
    return datetime.now(pytz.utc)  # Retorna o datetime no UTC


class Grupo_Produto(settings.Base):
    __tablename__ = "grupo_produto"  # Nome da tabela no banco de dados
    __table_args__ = {"extend_existing": True}  # Permite redefinir a tabela

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)

    usuario_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("usuario.id"), nullable=False, default=0
    )  # Chave estrangeira para a tabela 'usuario'

    # Relacionamento MANY-TO-ONE de Grupo_Produto para User (não 'Usuario')
    usuario: Mapped["User"] = relationship(
        "User",  # Referência correta à classe 'User'
        back_populates="grupo_produtos",  # Nome do campo de volta no User
        lazy="joined",
        uselist=True,  # Cada Grupo_Produto tem um único User
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=get_current_time_in_sp,  # timezone=True garante que seja "aware"
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=get_current_time_in_sp,
        onupdate=get_current_time_in_sp,
    )
    deleted_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime, nullable=True
    )  # Permite que seja None

    def __repr__(self) -> str:
        return f"<Grupo_Produto {self.name}>"