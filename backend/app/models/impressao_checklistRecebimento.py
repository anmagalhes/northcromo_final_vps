from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from app.database import Base  # Agora importa a base do SQLAlchemy de 'datapy'

class ImpressaoChecklistRecebimento(Base):
    __tablename__ = 'impressao_checklist_recebimento'
    __table_args__ = {'extend_existing': True} 

    id = Column(Integer, primary_key=True)  # Chave primária
    id_checklist = Column(Integer, ForeignKey('checklist_recebimento.id'), nullable=False)  # Chave estrangeira para 'checklist_recebimento'
    nome_cliente = Column(String(100), nullable=False)
    qtd_produto = Column(Numeric(10, 2), nullable=False)
    nome_produto = Column(String(100), nullable=False)
    referencia_produto = Column(String(50), nullable=False)
    nota_interna = Column(String(50), nullable=True)
    queixa_cliente = Column(String(255), nullable=True)
    data_rec_ordem_servicos = Column(DateTime, nullable=False)
    usuario_id = Column(Integer, ForeignKey('usuario.id'), nullable=False)  # Chave estrangeira para 'usuario'
    link_pdf_checklist = Column(String(255), nullable=True)
    recebimento_id = Column(Integer, ForeignKey('recebimentos.id'))  # Chave estrangeira para Recebimento

    # Relacionamentos
    checklist = relationship('ChecklistRecebimento', back_populates='impressao_checklists', lazy=True)
    recebimento = relationship("Recebimento", back_populates="impressao_checklists")

    # Relacionamento com o usuário
    usuario = relationship('User', back_populates='impressao_checklists', foreign_keys=[usuario_id], lazy='joined')

    # Colunas de controle de data
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<ImpressaoChecklistRecebimento id={self.id} nome_cliente={self.nome_cliente}>'
