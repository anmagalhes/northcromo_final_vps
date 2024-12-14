from datetime import datetime  # Importando o datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import validates, relationship  # Corrigido 'Relationship' para 'relationship'
from .db import db  # Importa a instância do db

class User(db.Model):  # A classe está correta com 'Usuarios' e não 'Usuario'
    __tablename__ = 'usuario'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    en_admin = db.Column(db.Boolean, default=False)  # Corrigido 'Columm' para 'Column'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Data de criação
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Data de última atualização
    deleted_at = db.Column(db.DateTime, nullable=True)  # Data de exclusão (soft delete)

     # Coluna para armazenar permissões ou configurações adicionais
    permissions = db.Column(db.JSON, default=[])  # Lista de permissões (ex: ['view', 'edit', 'delete'])
    extra_info = db.Column(db.JSON, nullable=True)  # Campo adicional para armazenar outras informações no formato JSON


    # Relacionamento: Um usuário pode ter vários grupos de produto
    grupo_produtos = relationship(
        "Grupo_Produto", 
        back_populates='criador', 
        uselist=True,
        lazy='joined'
        )
    
    # Relacionamento: Um usuário pode ter vários componentes
    componentes = relationship(
        "Componente", 
        back_populates='usuario',  # Define a relação bidirecional
        uselist=True,  # Indica que é uma relação de um-para-muitos
        lazy='joined'  # Lazy loading para otimizar a carga dos dados
    )

# Relacionamento: Um usuário pode ter vários componentes
    operacao = relationship(
        "Operacao", 
        back_populates='usuario',  # Define a relação bidirecional
        uselist=True,  # Indica que é uma relação de um-para-muitos
        lazy='joined'  # Lazy loading para otimizar a carga dos dados
    )

    # Relacionamento: Um usuário pode ter vários componentes
    posto_Trabalho = relationship(
        "Posto_Trabalho", 
        back_populates='usuario',  # Define a relação bidirecional
        uselist=True,  # Indica que é uma relação de um-para-muitos
        lazy='joined'  # Lazy loading para otimizar a carga dos dados
    )

     # Relacionamento com defeitos
    defeitos = relationship(
        "Defeito", 
        back_populates='usuario', 
        uselist=True,  # Indica que é uma relação de um-para-muitos
        lazy='joined')

     # Relacionamento com defeitos
    tarefa_Produto = relationship(
        "Tarefa_Produto", 
        back_populates='usuario', 
        uselist=True,  # Indica que é uma relação de um-para-muitos
        lazy='joined')
    
      # Relacionamento com defeitos
    recebimentos = relationship(
        "Recebimento", 
        back_populates='usuario', 
        uselist=True,  # Indica que é uma relação de um-para-muitos
        lazy='joined')
    
    # Relacionamento com defeitos
    fotoRecebimento = relationship(
        "FotoRecebimento", 
        back_populates='usuario', 
        uselist=True,  # Indica que é uma relação de um-para-muitos
        lazy='joined')
    
    # Relacionamento com defeitos
    produtos = relationship(
        "Produto", 
        back_populates='usuario', 
        uselist=True,  # Indica que é uma relação de um-para-muitos
        lazy='joined')
    
   
    

    def __repr__(self):
        return f'<User {self.username}>'
    
    @validates('created_at')
    def validate_created_at(self, key, value):
        """Valida e define o created_at"""
        return value or datetime.utcnow()

    @validates('updated_at')
    def validate_updated_at(self, key, value):
        """Valida e define o updated_at"""
        return value or datetime.utcnow()
