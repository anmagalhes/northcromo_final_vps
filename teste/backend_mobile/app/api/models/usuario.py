# app/api/models/usuario.py

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.base_class import Base
from app.api.models.base import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)

    # Relacionamento com recebimentos (se necessário)
    #recebimentos: Mapped[list["Recebimento"]] = relationship(back_populates="usuario")
