from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, JSON, ForeignKey, Numeric, Boolean
from typing import List, Optional

from sqlalchemy.orm import relationship
from sqlalchemy.orm import validates

from app.core.config import settings

class Operacao(settings.Base):
    __tablename__ = 'operacao'  # Nome da tabela no banco de dados
    __table_args__ = {'extend_existing': True} 

    id = Column(Integer, primary_key=True)
    grupo_processo = Column(String(5), unique=True, nullable=False)
    nome = Column(String(40), unique=True, nullable=False)
    usuario_id = Column(Integer, ForeignKey('usuario.id'))  # Chave estrangeira para 'usuarios'

   # Relacionamento: Agora utilizando o nome correto da classe 'User' (não 'Usuario')
    usuario = relationship("User", back_populates='operacao', foreign_keys=[usuario_id], lazy='joined')


    # Adicionando as colunas de data e hora
    created_at = Column(DateTime, default=datetime.utcnow)  # Data de criação
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Data de última atualização
    deleted_at = Column(DateTime, nullable=True)  # Data de exclusão (opcional para soft delete)

    def __repr__(self):
        return f'<operacao id={self.id} name={self.name}>'
        
