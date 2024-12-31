#app/modesl/produto.py
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm import relationship
from app.database import Base  # Agora importa a base do SQLAlchemy de 'database.py'

class Produto(Base):
    __tablename__ = 'produtos'
    __table_args__ = {'extend_existing': True} 

    id = Column(Integer, primary_key=True)
    cod_produto = Column(Integer, unique=True, nullable=False)
    nome_produto = Column(String(100), nullable=False)
    id_grupo = Column(Integer, ForeignKey('grupo_produto.id'))
    id_operacao_servico = Column(Integer, ForeignKey('posto_trabalho.id'))
    und_servicos = Column(String(50), nullable=False)
    hora_peca_servicos = Column(Float, nullable=True)
    id_componente = Column(Integer, ForeignKey('componente.id'))
    id_posto_trabalho = Column(Integer, ForeignKey('posto_trabalho.id'))
    fornec_produto = Column(String(100), nullable=True)
    estomin_produto = Column(Integer, nullable=True)
    und_medida_produto = Column(String(20), nullable=False)
    valor_unid_produto = Column(Float, nullable=False)
    controle_produto = Column(Boolean, default=True)
    status_produto = Column(String(20), nullable=False)
    tipo_produto = Column(String(50), nullable=False)
    origem_produto = Column(String(50), nullable=True)
    foto_produto = Column(String(255), nullable=True)
    data_cadastro_produto = Column(DateTime, default=datetime.utcnow)
    usuario_id = Column(Integer, ForeignKey('usuario.id'))
    tipo = Column(String(50), nullable=False)
    recebimento_id = Column(Integer, ForeignKey('recebimentos.id'))

    grupo_produto = relationship("Grupo_Produto", back_populates="produtos", lazy='joined')
    # Relacionamento com o posto de trabalho (id_posto_trabalho)
    posto_trabalho = relationship(
        "PostoTrabalho", 
        back_populates="produtos", 
        foreign_keys=[id_posto_trabalho],  # Especificando qual chave estrangeira utilizar
        lazy='joined'
    )
    # Relacionamento com operação de serviço (id_operacao_servico)
    operacao_servico = relationship(
        "PostoTrabalho", 
        back_populates="operacao_servico", 
        foreign_keys=[id_operacao_servico],  # Especificando qual chave estrangeira utilizar
        lazy='joined'
    )

    componente = relationship("Componente", back_populates="produtos", lazy='joined')
    checklists = relationship("ChecklistRecebimento", back_populates="produto", lazy='joined')
    usuario = relationship("User", back_populates="produtos", lazy='joined')
    recebimentos = relationship("Recebimento", back_populates="produto", foreign_keys="Recebimento.cod_produto", lazy='joined')

    def __repr__(self):
        return f'<Produto id={self.id} nome={self.nome_produto}>'
