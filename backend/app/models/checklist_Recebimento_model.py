from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from datetime import datetime 
from app.database import Base  # Agora importa a base do SQLAlchemy de 'datapy'

class ChecklistRecebimento(Base):
    __tablename__ = 'checklist_recebimento'
    __table_args__ = {'extend_existing': True}  # Permite redefinir a tabela


    id = Column(Integer, primary_key=True)
    id_Recebimento = Column(Integer, ForeignKey('recebimentos.id'), nullable=False)  # ID do recebimento
    id_cliente = Column(Integer, ForeignKey('clientes.id'), nullable=False)  # ID do cliente
    qtd_Produto = Column(Numeric(10, 2), nullable=False)  # Quantidade do produto
    cod_Produto = Column(Integer, ForeignKey('produtos.id'), nullable=False)  # Código do produto
    referencia_Produto = Column(String(50), nullable=False)  # Referência do produto
    notaInterna = Column(String(50), nullable=True)  # Nota interna (opcional)
    qUEIXA_CLIENTE = Column(String(255), nullable=True)  # Queixa do cliente (opcional)
    dataChecklist_OrdemServicos = Column(DateTime, nullable=False, default=datetime.utcnow)  # Data do checklist
    usuario_id = Column(Integer, ForeignKey('usuario.id'))  # Chave estrangeira de usuários
    LINK_PDF_CHECKLIST = Column(String(255), nullable=True)  # Link do PDF do checklist
    Status_Checklist = Column(String(50), nullable=False)  # Status do checklist (ex: 'Concluído', 'Em andamento', etc.)

    # Relacionamentos
    recebimento = relationship("Recebimento", back_populates="checklists")
    cliente = relationship("Cliente", back_populates="checklists")
    produto = relationship("Produto", back_populates="checklists")
    usuario = relationship("User", back_populates="checklists")
    
    # Removendo o backref e mantendo a relação explícita
    impressao_checklists = relationship("ImpressaoChecklistRecebimento", lazy=True)

    # Colunas de data e hora
    created_at = Column(DateTime, default=datetime.utcnow)  # Data de criação
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Data de última atualização
    deleted_at = Column(DateTime, nullable=True)  # Data de exclusão (opcional para soft delete)

    def __repr__(self):
        # Acessando o nome do produto carregado (mesmo com o lazy load)
        produto_nome = self.produto.nome if self.produto else 'Produto não encontrado'
        return f'<ChecklistRecebimento {self.referencia_Produto} - {produto_nome}>'
