# app/user/models.py
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import validates
from werkzeug.security import generate_password_hash, check_password_hash
from app.core.config import settings
from app.models.artigo import ArtigoModel

class User(settings.Base):  # Substituímos db.Model por Base
    __tablename__ = 'usuario'
    __table_args__ = {'extend_existing': True}  # Permite redefinir a tabela

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False, index=True)
    password = Column(String(128), nullable=False)
    en_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)
    #grupo_produto_id = Column(Integer, ForeignKey('grupo_produto.id'))  # Alterar para 'grupo_produto.id'
   # artigo_id = Column(Integer, ForeignKey('artigo.id'))

    # Coluna para armazenar permissões ou configurações adicionais
    permissions = Column(JSON, default=[])
    extra_info = Column(JSON, nullable=True)

    # Definindo o relacionamento com o modelo Artigo
    #artigos = relationship(
    #    "ArtigoModel",  # Isso refere-se a classe ArtigoModel
    #    back_populates="criador",
    #    lazy='joined'
    #)

    #grupo_produtos = relationship(
    #    "Grupo_Produto",
    #    back_populates="usuario",
    #    foreign_keys=[grupo_produto_id],
     #   lazy='joined'
    #)

    def __repr__(self):
        return f'<User {self.username}>'

"""
    # Relacionamentos
    clientes = relationship(
        "Cliente", 
        back_populates="usuario", 
        uselist=True,
        lazy='joined'
    )

    # A chave estrangeira do relacionamento foi especificada explicitamente
    #grupo_produtos = relationship(
    #    "Grupo_Produto",
    #    back_populates="usuario",
    #    foreign_keys=[grupo_produto_id],  # Explicitly specify the foreign key
    #    lazy='joined'
    #)

    componentes = relationship(
        "Componente", 
        back_populates='usuario', 
        lazy='joined'
    )

    operacao = relationship(
        "Operacao", 
        back_populates='usuario', 
        lazy='joined'
    )

    posto_trabalho = relationship(
        "PostoTrabalho", 
        back_populates="usuario", 
        lazy='joined'
    )

    defeitos = relationship(
        "Defeito", 
        back_populates='usuario', 
        lazy='joined'
    )

    tarefa_produto = relationship(
        "TarefaProduto", 
        back_populates="usuario", 
        lazy='joined'
    )
    
    recebimentos = relationship(
        "Recebimento", 
        back_populates='usuario', 
        lazy='joined'
    )

    produtos = relationship(
        "Produto", 
        back_populates='usuario', 
        lazy='joined'
    )

    checklists = relationship(
        "ChecklistRecebimento", 
        back_populates='usuario', 
        lazy='joined'
    )

    impressao_checklists = relationship(
        "ImpressaoChecklistRecebimento", 
        back_populates="usuario",  
        lazy='joined'
    )

    funcionarios = relationship(
        "Funcionario", 
        back_populates="usuario",  
        lazy='joined'
    )

    # Métodos para senha
    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)

    @validates('created_at')
    def validate_created_at(self, key, value):
        return value or datetime.utcnow()

    @validates('updated_at')
    def validate_updated_at(self, key, value):
        return value or datetime.utcnow()

"""
