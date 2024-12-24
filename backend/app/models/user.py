#app/user.py
from datetime import datetime  # Importando o datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import validates, relationship  # Corrigido 'Relationship' para 'relationship'
from werkzeug.security import generate_password_hash, check_password_hash  #
from app import db    # Importa a instância do db

class User(db.Model):  # A classe está correta com 'Usuarios' e não 'Usuario'
    __tablename__ = 'usuario'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    en_admin = db.Column(db.Boolean, default=False)  # Corrigido 'Columm' para 'Column'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Data de criação
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Data de última atualização
    deleted_at = db.Column(db.DateTime, nullable=True)  # Data de exclusão (soft delete)

     # Coluna para armazenar permissões ou configurações adicionais
    permissions = db.Column(db.JSON, default=[])  # Lista de permissões (ex: ['view', 'edit', 'delete'])
    extra_info = db.Column(db.JSON, nullable=True)  # Campo adicional para armazenar outras informações no formato JSON

    # Relacionamentos
    clientes = relationship(
         "Cliente", 
         back_populates="usuario", 
         lazy='select'
         )  # Relacionamento com Cliente

    # Relacionamento correto com 'Grupo_Produto' (garantir que a referência para 'Grupo_Produto' esteja correta)
    grupo_produtos = relationship(
        "Grupo_Produto", 
        back_populates='usuario', 
        uselist=True,
        lazy='joined'
    )
    
     # Relacionamento correto com 'componente'
    componentes = relationship(
        "Componente", 
        back_populates='usuario',  # Defina o 'back_populates' correto do lado do 'componente'
        uselist=True,
        lazy='joined'
    )

# Relacionamento: Um usuário pode ter vários componentes
    operacao = relationship(
        "Operacao", 
        back_populates='usuario',  # Define a relação bidirecional
        uselist=True,  # Indica que é uma relação de um-para-muitos
        lazy='joined'  # Lazy loading para otimizar a carga dos dados
    )

    # Relacionamento com Posto_Trabalho
    posto_trabalho = db.relationship(
        "PostoTrabalho",  # Nome correto da classe 'PostoTrabalho'
        back_populates="usuario",  # Relacionamento inverso
        uselist=True,  # Relacionamento de um para muitos
        lazy='joined'  # Lazy loading
    )

     # Relacionamento com defeitos
    defeitos = relationship(
        "Defeito", 
        back_populates='usuario', 
        uselist=True,  # Indica que é uma relação de um-para-muitos
        lazy='joined')

     # Relacionamento com TarefaProduto
    tarefa_produto = db.relationship(
        "TarefaProduto",  # Nome correto da classe 'TarefaProduto'
        back_populates="usuario",  # Relacionamento inverso
        uselist=True,  # Relacionamento de um para muitos
        lazy='joined'  # Lazy loading
    )
    
      # Relacionamento com defeitos
    recebimentos = relationship(
        "Recebimento", 
        back_populates='usuario', 
        uselist=True,  # Indica que é uma relação de um-para-muitos
        lazy='joined')
    
    # Relacionamento com defeitos
    produtos = relationship(
        "Produto", 
        back_populates='usuario', 
        lazy='joined')
    
    # Relacionamento com defeitos
    checklists  = relationship(
        "ChecklistRecebimento", 
        back_populates='usuario', 
        uselist=True,  # Indica que é uma relação de um-para-muitos
        lazy='joined')
    
     # Relacionamento: Um usuário pode ter vários 'ImpressaoChecklistRecebimento'
    impressao_checklists = relationship(
        "ImpressaoChecklistRecebimento", 
        back_populates="usuario",  # Relacionamento inverso
        uselist=True, 
        lazy='joined'
    )

     # Relacionamento com 'Funcionario'
    funcionarios = relationship(
        "Funcionario", 
        back_populates="usuario",  # Nome do relacionamento na classe Funcionario
        uselist=True,  # Relação de um para muitos
        lazy='joined'  # Lazy loading para otimizar a carga dos dados
    )
    
    # Método para definir a senha (transforma em hash)
    def set_password(self, password):
        """Transforma a senha fornecida em um hash e armazena"""
        self.password = generate_password_hash(password)  # Gera o hash da senha
    
    # Método para verificar a senha durante o login
    def check_password(self, password):
        """Verifica a senha fornecida com o hash armazenado"""
        return check_password_hash(self.password, password)  # Verifica se o hash da senha bate
    
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
    
    def __repr__(self):
            return f'<User {self.username}>'