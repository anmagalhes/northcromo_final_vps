# app/models.py
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, JSON, ForeignKey, Numeric, Boolean
from typing import List, Optional

from sqlalchemy.orm import relationship
from sqlalchemy.orm import validates

from app.core.config import settings

class Grupo_Produto(settings.Base):
    __tablename__ = 'grupo_produto'  # Nome da tabela no banco de dados
    __table_args__ = {'extend_existing': True}  # Permite redefinir a tabela

    

    id = Column(Integer, primary_key=True)
    name = Column(String(20), unique=True, nullable=False)
    usuario_id = Column(Integer, ForeignKey('user.id'))  # Chave estrangeira para 'usuarios'
    
    # Relacionamento com 'User'
    #usuario = relationship(
    #    "User",
    #    back_populates='grupo_produtos',
    #    foreign_keys=[usuario_id]  # Explicitly specify the foreign key
    #)

    # Relacionamento com 'Componente'
    componentes = relationship("Componente", back_populates="grupo_produto", lazy='joined')
    
    # Relacionamento com 'Produto'
    produtos = relationship("Produto", back_populates="grupo_produto", lazy='joined')

    created_at = Column(DateTime, default=datetime.utcnow)  # Data de criação
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Data de última atualização
    deleted_at = Column(DateTime, nullable=True)  # Data de exclusão (opcional para soft delete)

    def __repr__(self):
        return f'<Grupo_Produto id={self.id} name={self.name}>'
