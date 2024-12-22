# app/models/grupo_produto
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .db import db  # Importando a instância do db

class Grupo_Produto(db.Model):
    __tablename__ = 'grupo_produto'  # Nome da tabela no banco de dados

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    usuario_id = db.Column(db.Integer, ForeignKey('usuario.id'))  # Chave estrangeira para 'usuarios'
    
    # Relacionamento: Agora utilizando o nome correto da classe 'User' (não 'Usuario')
    usuario = relationship("User", back_populates='grupo_produtos', foreign_keys=[usuario_id], lazy='joined')
    
    # Relacionamento com 'componente_1'
    componentes = relationship("Componente", back_populates="grupo_produto", lazy='joined')
    
    # Relacionamento com a tabela Produto
    produtos = relationship("Produto", back_populates="grupo_produto", lazy='joined')


    # Adicionando as colunas de data e hora
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Data de criação
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Data de última atualização
    deleted_at = db.Column(db.DateTime, nullable=True)  # Data de exclusão (opcional para soft delete)

    def __repr__(self):
        return f'<Grupo_Produto id={self.id} name={self.name}>'

