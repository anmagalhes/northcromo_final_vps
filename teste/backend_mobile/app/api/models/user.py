# app/models/user.py
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

from app.models.grupo_produto import Grupo_Produto
from app.models.cliente import Cliente
from app.models.todo import Todo
from app.models.componente import Componente
from app.models.postotrabalho import Postotrabalho
from app.models.posto_tarefa import Postotarefa
from app.models.operacao import Operacao
from app.models.defeito import Defeito
from app.models.produto import Produto
from app.models.recebimento.recebimento import Recebimento
from app.models.recebimento.itens_recebimento import ItensRecebimento
from app.models.notafiscal.notafiscal import NotaFiscal
from app.models.notafiscal.notaRecebimento import NotaRecebimento
from app.models.checklist_recebimento.checklist_recebimento import Checklist_Recebimento
from app.models.funcionario import Funcionario

# Criando um timezone para São Paulo (UTC-3)
SP_TZ = pytz.timezone("America/Sao_Paulo")


# Função auxiliar para garantir o uso correto do timezone
def get_current_time_in_sp() -> datetime:
    return datetime.now(SP_TZ).astimezone(
        SP_TZ
    )  # Garante que a data e hora sejam "aware"


# Alternativa: utilizar UTC
def get_current_time_in_utc() -> datetime:
    return datetime.now(pytz.utc)  # Retorna o datetime no UTC


class User(settings.Base):  # Substituímos db.Model por Base
    __tablename__ = "usuario"
    __table_args__ = {"extend_existing": True}  # Permite redefinir a tabela

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(128), nullable=False)
    en_admin: Mapped[bool] = mapped_column(Boolean, default=False)
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

    # Colunas para armazenar permissões ou configurações adicionais
    # permissions: Mapped[List[str]] = mapped_column(
    #    JSON, default=list, nullable=True
    # )  # Usando list() em vez de []
    # extra_info: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)

    # Relacionamento ONE-TO-MANY de Usuario para Grupo_Produto
    grupo_produtos: Mapped[List["Grupo_Produto"]] = relationship(
        "Grupo_Produto",  # Nome da classe de destino
        back_populates="usuario",  # Nome do campo de volta no Grupo_Produto
    )

    # Relacionamentos com o modelo clientes
    clientes: Mapped[List["Cliente"]] = relationship(
        "Cliente",
        back_populates="usuario",
    )

    # Relacionamentos com o modelo clientes
    todos: Mapped[List["Todo"]] = relationship(
        "Todo",
        back_populates="usuario",
    )

    # Relacionamentos com o modelo clientes
    componentes: Mapped[List["Componente"]] = relationship(
        "Componente",
        back_populates="usuario",
    )

    # Relacionamentos com o modelo clientes
    Postotrabalhos: Mapped[List["Postotrabalho"]] = relationship(
        "Postotrabalho",
        back_populates="usuario",
    )

    # Relacionamento com Postotarefa
    Postotarefas: Mapped[List["Postotarefa"]] = relationship(
        "Postotarefa",  # Nome da classe de destino
        back_populates="usuario",  # Nome do campo de volta no Postotarefa
    )

    # Relacionamento com 'Operacao' (caso esteja faltando)
    Operacoes: Mapped[List["Operacao"]] = relationship(
        "Operacao",  # Nome da classe de destino
        back_populates="usuario",  # Nome do campo de volta em Operacao
    )

    # Relacionamento com 'Operacao' (caso esteja faltando)
    Defeitos: Mapped[List["Defeito"]] = relationship(
        "Defeito",  # Nome da classe de destino
        back_populates="usuario",  # Nome do campo de volta em Operacao
    )

    # Relacionamento com Produto
    produtos: Mapped[List["Produto"]] = relationship(
        "Produto",  # Nome da classe de destino
        back_populates="usuario",  # Nome do campo de volta em Operacao
    )

    # Relacionamento com a tabela Recebimento (um usuário pode ter muitos recebimentos)
    recebimentos: Mapped[List["Recebimento"]] = relationship(
        "Recebimento",  # Relacionamento com Recebimento (um-para-muitos)
        back_populates="usuario",  # Referência ao campo `usuario` em Recebimento
    )

    checklist: Mapped[List["Checklist_Recebimento"]] = relationship(
        "Checklist_Recebimento",  # Relacionamento com Recebimento (um-para-muitos)
        back_populates="usuario",  # Referência ao campo `usuario` em Recebimento
    )

    # Relacionamento MANY-TO-ONE de Grupo_Produto para User (não 'Usuario')
    funcionario: Mapped["Funcionario"] = relationship(
        "Funcionario",  # Referência correta à classe 'User'
        back_populates="usuario",  # Nome do campo de volta no User
    )

    def __repr__(self) -> str:
        return f"<User {self.username}>"
