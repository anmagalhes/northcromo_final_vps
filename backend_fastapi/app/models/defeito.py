from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, JSON, ForeignKey, Numeric
from typing import List, Optional

from sqlalchemy.orm import relationship
from sqlalchemy.orm import validates

from app.core.config import settings

class Defeito(settings.Base):
    __tablename__ = 'defeito'  # Nome da tabela no banco de dados
    __table_args__ = {'extend_existing': True}  # Permite redefinir, não cria nova tabela
    
    id = Column(Integer, primary_key=True)
    nome = Column(String(40), unique=True, nullable=False)
    usuario_id = Column(Integer, ForeignKey('usuario.id'))  # Chave estrangeira para 'usuario'
    componente_id = Column(Integer, ForeignKey('componente.id'))  # Chave estrangeira para 'componente'

    # Relacionamento com 'User' (certifique-se de que a classe seja 'User' e não 'Usuario')
    usuario = relationship("User", back_populates='defeitos', foreign_keys=[usuario_id], lazy='joined')

    # Relacionamento com 'Componente' (nome correto da tabela é 'componente')
    componente = relationship("Componente", back_populates='defeitos', lazy='joined')

    # Adicionando as colunas de data e hora
    created_at = Column(DateTime, default=datetime.utcnow)  # Data de criação
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Data de última atualização
    deleted_at = Column(DateTime, nullable=True)  # Data de exclusão (opcional para soft delete)

    def __repr__(self):
        return f'<Defeito id={self.id} nome={self.nome}>'
    
    # Método to_dict para converter o objeto em um dicionário
    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "usuario_id": self.usuario_id,
            "componente_id": self.componente_id,
            "componente_nome": self.componente.nome if self.componente else None,  # Adicionando o nome do componente
            "usuario_nome": self.usuario.nome if self.usuario else None,  # Adicionando o nome do usuário
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "deleted_at": self.deleted_at
        }

