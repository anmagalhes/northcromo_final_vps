# app/models/PostoTrabalho.py
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app import db    # Importando a instância do db

class PostoTrabalho(db.Model):
    __tablename__ = 'posto_trabalho'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(40), unique=True, nullable=False)
    usuario_id = db.Column(db.Integer, ForeignKey('usuario.id'))

    usuario = relationship("User", back_populates='posto_trabalho', foreign_keys=[usuario_id], lazy='joined')

    # Relacionamentos com produtos
    produtos = relationship(
        'Produto', 
        back_populates='posto_trabalho', 
        foreign_keys='Produto.id_posto_trabalho',  # Especificando qual coluna usar para o relacionamento
        lazy='joined'
    )

    operacao_servico = relationship(
        'Produto', 
        back_populates='posto_trabalho', 
        foreign_keys='Produto.id_operacao_servico',  # Especificando qual coluna usar para o relacionamento
        lazy='joined'
    )

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f'<PostoTrabalho id={self.id} nome={self.nome}>'
