from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .db import db  # Importando a instância do db

class PostoTrabalho(db.Model):
    __tablename__ = 'posto_trabalho'  # Nome correto da tabela no banco de dados

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(40), unique=True, nullable=False)
    usuario_id = db.Column(db.Integer, ForeignKey('usuario.id'))  # Chave estrangeira para 'usuario'

    # Relacionamento com a tabela Usuario
    usuario = relationship("User", back_populates='posto_trabalho', lazy='joined')  # Verifique se o modelo é 'User' (não 'users')
    produtos = relationship('Produto', back_populates='posto_trabalho', lazy='joined')
    operacao_servico = relationship('Produto', back_populates='posto_trabalho', lazy='joined')

    # Adicionando as colunas de data e hora
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Data de criação
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Data de última atualização
    deleted_at = db.Column(db.DateTime, nullable=True)  # Data de exclusão (opcional para soft delete)

    def __repr__(self):
        return f'<PostoTrabalho id={self.id} name={self.name}>'

