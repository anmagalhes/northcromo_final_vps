# app/user/models.py
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, JSON, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.orm import validates
from werkzeug.security import generate_password_hash, check_password_hash
from app.core.config import settings
from app.models.artigo import ArtigoModel


class User(settings.Base):  # Substituímos db.Model por Base
    __tablename__ = 'usuario'
    __table_args__ = {'extend_existing': True}  # Permite redefinir a tabela

      # Usando Mapped e mapped_column para definir as colunas
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False, index=True)
    password: Mapped[str] = mapped_column(String(128), nullable=False)
    en_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)  # Permite que seja None

    # Relacionamentos com outras tabelas
    #grupo_produto_id: Mapped[int] = mapped_column(Integer, ForeignKey('grupo_produto.id'))  # Relacionamento com GrupoProduto
    #artigo_id: Mapped[int] = mapped_column(Integer, ForeignKey('artigo.id'))  # Relacionamento com ArtigoModel

    # Relacionamentos (se houver)
    # grupo_produto: Mapped["GrupoProdutoModel"] = relationship("GrupoProdutoModel", backref="usuarios")
    # artigo: Mapped["ArtigoModel"] = relationship("ArtigoModel", backref="usuarios")

    # Colunas para armazenar permissões ou configurações adicionais
    permissions: Mapped[list] = mapped_column(JSON, default=[])
    extra_info: Mapped[dict | None] = mapped_column(JSON, nullable=True)

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
