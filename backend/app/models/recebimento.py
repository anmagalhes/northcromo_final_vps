from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from app.database import Base  # Agora importa a base do SQLAlchemy de 'datapy'

class Recebimento(Base):
    __tablename__ = 'recebimentos'
    __table_args__ = {'extend_existing': True}  # Permite redefinir a tabela


    id = Column(Integer, primary_key=True)
    id_ordem = Column(String(9), nullable=False)  # Número da ordem
    tipo_ordem = Column(String(4), nullable=False)  # Tipo da ordem
    id_cliente = Column(Integer, ForeignKey('clientes.id'), nullable=False)  # Chave estrangeira para Cliente
    qtd_produto = Column(Numeric(10, 2), nullable=False)  # Quantidade do produto
    cod_produto = Column(Integer, ForeignKey('produtos.id'), nullable=False)  # Chave estrangeira para Produto
    referencia_produto = Column(String(50), nullable=False)  # Referência do produto
    nota_interna = Column(String(50), nullable=True)  # Nota interna (opcional)
    vendedor_id = Column(Integer, ForeignKey('funcionarios.id'))  # Chave estrangeira para Funcionario
    queixa_cliente = Column(String(255), nullable=True)  # Queixa do cliente (opcional)
    status_ordem = Column(String(50), nullable=True)  # Status da ordem (opcional)
    data_cadastro = Column(DateTime, nullable=False, default=datetime.utcnow)  # Data de cadastro
    usuario_id = Column(Integer, ForeignKey('usuario.id'), nullable=False)  # Chave estrangeira para Usuario

    # Relacionamentos
    cliente = relationship("Cliente", back_populates="recebimentos", lazy='joined')  # Relacionamento com Cliente
    produto = relationship("Produto", back_populates="recebimentos", foreign_keys=[cod_produto], lazy='joined')  # Relacionamento com Produto
    usuario = relationship("User", back_populates="recebimentos", foreign_keys=[usuario_id], lazy='joined')  # Relacionamento com Usuario
    funcionario = relationship('Funcionario', back_populates='recebimentos_cadastrados', lazy='joined')  # Relacionamento com Funcionario
    checklists = relationship("ChecklistRecebimento", back_populates="recebimento", lazy='joined')  # Relacionamento com ChecklistRecebimento
    impressao_checklists = relationship("ImpressaoChecklistRecebimento", back_populates="recebimento", lazy='joined')
    fotos = relationship("FotoRecebimento", back_populates="ordem", lazy='joined')
    
    # Colunas de data e hora
    created_at = Column(DateTime, default=datetime.utcnow)  # Data de criação
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Data de última atualização
    deleted_at = Column(DateTime, nullable=True)  # Data de exclusão (opcional para soft delete)

    def __repr__(self):
        return f'<Recebimento id={self.id} ordem={self.id_ordem}>'