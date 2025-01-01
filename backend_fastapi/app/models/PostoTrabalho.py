# app/models/PostoTrabalho.py
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm import relationship
from app.database import Base  # Agora importa a base do SQLAlchemy de 'datapy'


class PostoTrabalho(Base):
    __tablename__ = "posto_trabalho"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)
    nome = Column(String(40), unique=True, nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuario.id"))

    usuario = relationship(
        "User",
        back_populates="posto_trabalho",
        foreign_keys=[usuario_id],
        lazy="joined",
    )

    # Relacionamentos com produtos
    produtos = relationship(
        "Produto",
        back_populates="posto_trabalho",
        foreign_keys="Produto.id_posto_trabalho",  # Especificando qual coluna usar para o relacionamento
        lazy="joined",
    )

    operacao_servico = relationship(
        "Produto",
        back_populates="posto_trabalho",
        foreign_keys="Produto.id_operacao_servico",  # Especificando qual coluna usar para o relacionamento
        lazy="joined",
    )

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<PostoTrabalho id={self.id} nome={self.nome}>"
