from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .db import db  # Importando a instância do db

class Componente(db.Model):
    __tablename__ = 'componente'  # Nome da tabela no banco de dados

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(40), unique=True, nullable=False)  # Alterado de 'name' para 'nome'
    usuario_id = db.Column(db.Integer, ForeignKey('usuario.id'))  # Chave estrangeira para 'usuario'
    grupo_produto_id = db.Column(db.Integer, ForeignKey('grupo_produto.id'))  # Relacionamento com 'Grupo_Produto'
    
    # Relacionamento com 'User'
    usuario = relationship("User", back_populates="componentes", foreign_keys=[usuario_id], lazy='joined')

    # Relacionamento com 'Grupo_Produto'
    grupo_produto = relationship("Grupo_Produto", back_populates="componentes", lazy='joined')
    
    # Relacionamento com 'Defeito'
    defeitos = relationship(
        "Defeito", 
        back_populates='componente', 
        uselist=True,  # Indica que é uma relação de um-para-muitos
        lazy='joined'
    )
    
    # Relacionamento com 'Produto'
    produtos = relationship(
        "Produto", 
        back_populates='componente', 
        uselist=True,  # Indica que é uma relação de um-para-muitos
        lazy='joined'
    )

    # Colunas de controle de data
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Data de criação
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Data de última atualização
    deleted_at = db.Column(db.DateTime, nullable=True)  # Data de exclusão (opcional para soft delete)

    def __repr__(self):
        return f'<Componente id={self.id} nome={self.nome if self.nome else "Unnamed"}>'
