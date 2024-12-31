# app/models/user.py
from datetime import datetime
import pytz

from sqlalchemy import JSON, Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.config import settings

from typing import Optional 

#from models.clientes import clientes
#from app.models.grupo_produto import Grupo_Produto

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

     # Relacionamento com Grupo_Produto
    grupo_produto_id: Mapped[int] = mapped_column(Integer, ForeignKey('grupo_produto.id', name='fk_usuario_grupo_produto'))
    grupo_produto: Mapped["Grupo_Produto"] = relationship("Grupo_Produto", back_populates="usuarios", lazy='joined')

    # Relacionamentos com o modelo clientes
    clientes_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('clientes.id', name='fk_usuario_clientes'), nullable=True)
    clientes: Mapped["cliente"] = relationship("cliente", back_populates="usuario", lazy="joined")

    # Relacionamento com o modelo Recebimento (importação tardia)
    recebimentos: Mapped[list] = relationship("Recebimento", back_populates="usuario", lazy="joined")

    # Colunas para armazenar permissões ou configurações adicionais
    permissions: Mapped[list] = mapped_column(JSON, default=[])
    extra_info: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    def __repr__(self) -> str:
        return f"<User {self.username}>"