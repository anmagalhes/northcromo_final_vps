# app/models/user.py
from datetime import datetime
import pytz

from sqlalchemy import JSON, Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.config import settings

from typing import Optional, List

# Criando um timezone para São Paulo (UTC-3)
SP_TZ = pytz.timezone("America/Sao_Paulo")

class User(settings.Base):  # Substituímos db.Model por Base
    __tablename__ = "usuario"
    __table_args__ = {"extend_existing": True}  # Permite redefinir a tabela

    # Usando Mapped e mapped_column para definir as colunas
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(128), nullable=False)
    en_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(SP_TZ))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(SP_TZ), onupdate=lambda: datetime.now(SP_TZ)
    )
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)  # Permite que seja None

    # Colunas para armazenar permissões ou configurações adicionais
    permissions: Mapped[list] = mapped_column(JSON, default=[])
    extra_info: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    # Relacionamento ONE-TO-MANY de Usuario para Grupo_Produto
    grupo_produtos: Mapped[List["Grupo_Produto"]] = relationship(
        "Grupo_Produto",  # Nome da classe de destino
        back_populates="usuario",  # Nome do campo de volta no Grupo_Produto
        lazy='joined'  # Pode ajustar para o comportamento de carregamento desejado
    )

    # Relacionamentos com o modelo clientes
    clientes: Mapped["Cliente"] = relationship(
        "Cliente", 
        back_populates="usuario", 
        lazy="joined"
        )
    
    def __repr__(self) -> str:
        return f"<User {self.username}>"