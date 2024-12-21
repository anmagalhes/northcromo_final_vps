from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .db import db  # Importando a instância do db

class Defeito(db.Model):
    __tablename__ = 'defeito'  # Nome da tabela no banco de dados

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(40), unique=True, nullable=False)
    usuario_id = db.Column(db.Integer, ForeignKey('usuario.id'))  # Chave estrangeira para 'usuarios'
    componente_id = db.Column(db.Integer, ForeignKey('componente.id'))  # Chave estrangeira para 'componente_1'

     # Relacionamento: Agora utilizando o nome correto da classe 'User' (não 'Usuario')
    usuario = relationship("User", back_populates='defeitos', foreign_keys=[usuario_id], lazy='joined')

     # Relacionamento com o componente
    componente = relationship("Componente", back_populates='defeitos', lazy='joined')

    # Adicionando as colunas de data e hora
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Data de criação
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Data de última atualização
    deleted_at = db.Column(db.DateTime, nullable=True)  # Data de exclusão (opcional para soft delete)

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
