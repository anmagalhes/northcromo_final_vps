# app/models/cliente.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base  # Agora importa a base do SQLAlchemy de 'datapy'

class Cliente(Base):
    __tablename__ = 'clientes'  # Nome da tabela no banco de dados

    id = Column(Integer, primary_key=True)  # ID do Cliente (obrigatório)
    
    # Colunas obrigatórias
    tipo_cliente = Column(String(50), nullable=True)  # Tipo de Cliente
    nome_cliente = Column(String(100), nullable=True)  # Nome do Cliente
    doc_cliente = Column(String(20), nullable=True)  # Documento do Cliente (CPF/CNPJ)
    endereco_cliente = Column(String(255), nullable=True)  # Endereço do Cliente
    num_cliente = Column(String(20), nullable=True)  # Número do endereço
    bairro_cliente = Column(String(100), nullable=True)  # Bairro
    cidade_cliente = Column(String(100), nullable=True)  # Cidade
    uf_cliente = Column(String(2), nullable=True)  # UF
    cep_cliente = Column(String(10), nullable=True)  # CEP
    telefone_cliente = Column(String(20), nullable=True)  # Telefone do Cliente
    
    # Colunas que podem ser nulas (não obrigatórias)
    telefone_rec_cliente = Column(String(20), nullable=True)  # Telefone de recado
    whatsapp_cliente = Column(String(20), nullable=True)  # WhatsApp
    email_funcionario = Column(String(100), nullable=True)  # E-mail do Funcionário responsável
    acao = Column(String(255), nullable=True)  # Ação/observações adicionais
    fornecedor_cliente = Column(String(100), nullable=True)  # Fornecedor associado ao cliente

    # Colunas de datas
    data_cadastro_cliente = Column(DateTime, default=datetime.utcnow)  # Data de cadastro
    created_at = Column(DateTime, default=datetime.utcnow)  # Data de criação
    updated_at = Column(DateTime, onupdate=datetime.utcnow)  # Data de atualização
    usuario_id = Column(Integer, ForeignKey('usuario.id'))  # Chave estrangeira de usuários

    # Relacionamentos
    usuario = relationship("User", back_populates="clientes", lazy='joined')
    recebimentos = relationship("Recebimento", back_populates="cliente", lazy='joined')
    checklists = relationship("ChecklistRecebimento", back_populates="cliente", lazy='joined')

    def __repr__(self):
        return f'<Cliente {self.nome_cliente}>'

    def to_json(self, include_relations=False):
        """Retorna os dados do cliente, com opção de excluir relacionamentos"""
        client_json = {
            "id": self.id,
            "tipo_cliente": self.tipo_cliente,
            "nome_cliente": self.nome_cliente,
            "doc_cliente": self.doc_cliente,
            "endereco_cliente": self.endereco_cliente,
            "num_cliente": self.num_cliente,
            "bairro_cliente": self.bairro_cliente,
            "cidade_cliente": self.cidade_cliente,
            "uf_cliente": self.uf_cliente,
            "cep_cliente": self.cep_cliente,
            "telefone_cliente": self.telefone_cliente,
            "telefone_rec_cliente": self.telefone_rec_cliente,
            "whatsapp_cliente": self.whatsapp_cliente,
            "data_cadastro_cliente": self.data_cadastro_cliente,
            "fornecedor_cliente": self.fornecedor_cliente,
            "email_funcionario": self.email_funcionario,
            "acao": self.acao,
            "usuario_id": self.usuario_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
        
        if include_relations:
                    # Adiciona relacionamentos caso necessário
                    client_json["usuario"] = self.usuario.to_json() if self.usuario else None
                    client_json["recebimentos"] = [recebimento.to_json() for recebimento in self.recebimentos]
                    client_json["checklists"] = [checklist.to_json() for checklist in self.checklists]

        return client_json

