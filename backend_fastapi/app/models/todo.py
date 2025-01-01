# app/models/todo.py
from datetime import datetime
import pytz
from enum import Enum

from sqlalchemy import (
    JSON,
    Boolean,
    DateTime,
    Integer,
    String,
    ForeignKey,
    Table,
    Column,
    Enum as SAEnum,
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


class TodoState(str, Enum):
    draf = "draft"
    todo = "todo"
    doing = "doing"
    done = "done"
    trash = "trash"


class Todo(settings.Base):  # Substituímos db.Model por Base
    __tablename__ = "todos"
    __table_args__ = {"extend_existing": True}  # Permite redefinir a tabela

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)  # a
    titulo: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    descricao: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    status: Mapped[TodoState] = mapped_column(SAEnum(TodoState), nullable=True)

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

    # Relacionamento com o modelo User (usando tipagem de string)
    usuario_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("usuario.id"), nullable=True
    )  # Tabela Campo

    # Relacionamento MANY-TO-ONE de Grupo_Produto para User (não 'Usuario')
    usuario: Mapped["User"] = relationship(
        "User",  # Referência correta à classe 'User'
        back_populates="todos",  # Nome do campo de volta no User
        lazy="joined",
    )

    def __repr__(self):
        return f"Todo(id={self.id}, titulo={self.titulo}, status={self.status})"
