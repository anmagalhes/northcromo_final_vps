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
    usuario = relationship("User", back_populates="funcionarios")  # Corrigido para usar 'User' e 'funcionarios'

    nivel_acesso = db.Column(db.String(50), nullable=False)  # Nível de acesso do funcionário
    acao = db.Column(db.String(100), nullable=True)  # Ações/observações adicionais

    # Relacionamento com Recebimentos (como vendedor, por exemplo)
    recebimentos_cadastrados = relationship(
        "Recebimento", 
        back_populates="funcionario",  # O 'back_populates' na classe Recebimento já foi configurado corretamente
        uselist=True,  # Relação de um-para-muitos
        lazy='joined'  # Lazy loading para otimizar a carga dos dados
    )

    def __repr__(self):
        return f'<Funcionario id={self.id} name={self.name}>'
