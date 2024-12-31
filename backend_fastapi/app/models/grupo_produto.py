# app/models/grupo_produto
from datetime import datetime
import pytz

from sqlalchemy import JSON, Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.config import settings
from models.user import User

# Criando um timezone para São Paulo (UTC-3)
SP_TZ = pytz.timezone("America/Sao_Paulo")


class Grupo_Produto(settings.Base):
    __tablename__: str = 'grupo_produto'  # Nome da tabela no banco de dados
    __table_args__ = {'extend_existing': True}  # Permite redefinir a tabela

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    usuario_id: Mapped[str] = mapped_column(Integer, ForeignKey('usuario.id')) # Tabela Campo
    
    # Relacionamento com 'User'
    usuario: Mapped["User"] = relationship(  # Aqui você usa a string "User"
        "User",  # A classe 'User'
        back_populates="grupos_produto",  # Relacionamento bidirecional
        lazy='joined'
    )

    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(SP_TZ))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(SP_TZ), onupdate=lambda: datetime.now(SP_TZ)
    )
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True
    )  # Permite que seja None
    
    def __repr__(self) -> str:
        return f"<Grupo_produto {self.name}>"