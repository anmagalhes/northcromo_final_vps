from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .db import db  # Importando a instância do db

class Componente(db.Model):
    __tablename__ = 'componente'  # Nome da tabela no banco de dados

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True, nullable=False)
    usuario_id = db.Column(db.Integer, ForeignKey('usuario.id'))  # Chave estrangeira para 'usuarios'

    # Relacionamento: Cada grupo de produto pertence a um usuário
    usuario = relationship("Users", back_populates='defeitos', lazy='joined')

    # Relacionamento com defeitos
    defeitos = relationship(
        "Defeito", 
        back_populates='componente', 
        uselist=True,  # Indica que é uma relação de um-para-muitos
        lazy='joined')
    
        # Relacionamento com defeitos
    produtos = relationship(
        "Produto", 
        back_populates='componente', 
        uselist=True,  # Indica que é uma relação de um-para-muitos
        lazy='joined')


    # Adicionando as colunas de data e hora
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Data de criação
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Data de última atualização
    deleted_at = db.Column(db.DateTime, nullable=True)  # Data de exclusão (opcional para soft delete)

    def __repr__(self):
        return f'<Componente {self.name}>'