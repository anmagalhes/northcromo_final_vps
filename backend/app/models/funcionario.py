from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .db import db  # Importando a instância do db

class Funcionario(db.Model):
    __tablename__ = 'funcionarios'  # Nome da tabela no banco de dados

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    funcao = db.Column(db.String(50), nullable=False)
    setor = db.Column(db.String(50), nullable=False)
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)
    acesso_sistema = db.Column(db.Boolean, default=True)  # Se tem acesso ao sistema
    usuario_id = db.Column(db.Integer, ForeignKey('usuario.id'))  # Chave estrangeira de usuários
    usuario = relationship("Users", back_populates="funcionario")  # Relacionamento com Usuários

    nivel_acesso = db.Column(db.String(50), nullable=False)  # Nível de acesso do funcionário
    acao = db.Column(db.String(100), nullable=True)  # Ações/observações adicionais

    def __repr__(self):
        return f'<Funcionario {self.nome}>'