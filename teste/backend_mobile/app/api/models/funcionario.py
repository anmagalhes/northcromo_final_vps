from datetime import datetime
from sqlalchemy import Integer, String, DateTime, ForeignKey, Boolean, func, Column, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.api.models.base import Base
from app.api.models.mixins import TimestampMixin

from  app.api.models.enums import StatusEnum  # importe o enum correto

class Funcionario(Base, TimestampMixin):
    __tablename__ = "funcionarios"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    telefone: Mapped[str] = mapped_column(String(20), nullable=True)
    email: Mapped[str] = mapped_column(String(100), nullable=True)

    # ForeignKey para a tabela funcoes
    funcao_id: Mapped[int] = mapped_column(ForeignKey("funcoes.id"), nullable=False)
    funcao_rel: Mapped["Funcao"] = relationship("Funcao", back_populates="funcionarios", lazy="joined")

    # Removido o setor, pois você mencionou que não vai usar
    data_cadastro: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    acesso_sistema: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id", ondelete="SET NULL"), nullable=True)
    usuario: Mapped["Usuario"] = relationship("Usuario", lazy="joined")

    status = Column(Enum(StatusEnum), nullable=False, default=StatusEnum.ATIVO)

    def __repr__(self):
        funcao_nome = self.funcao_rel.funcao_nome if self.funcao_rel else None
        return f"<Funcionario(nome={self.nome}, funcao={funcao_nome}, acesso_sistema={self.acesso_sistema})>"
