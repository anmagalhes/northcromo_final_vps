# app/models/cliente_model.py
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, JSON, ForeignKey, Numeric
from typing import List, Optional

from sqlalchemy.orm import relationship
from sqlalchemy.orm import validates

from app.core.config import settings

from app.models.user import User
from app.models.recebimento import Recebimento
from app.models.checklist_Recebimento import Checklist

class Cliente(settings.Base):
    __tablename__ = 'clientes'  # Nome da tabela no banco de dados
    __table_args__ = {'extend_existing': True}  # Permite redefinir a tabela

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    tipo_cliente: Optional[str] = Column(String(50), nullable=True)  # Tipo de Cliente
    nome_cliente: str = Column(String(100), nullable=True)  # Nome do Cliente
    doc_cliente: str = Column(String(20), nullable=True)  # Documento do Cliente (CPF/CNPJ)
    endereco_cliente: str = Column(String(255), nullable=True)  # Endereço do Cliente
    num_cliente: str = Column(String(20), nullable=True)  # Número do endereço
    bairro_cliente: str = Column(String(100), nullable=True)  # Bairro
    cidade_cliente: str = Column(String(100), nullable=True)  # Cidade
    uf_cliente: str = Column(String(2), nullable=True)  # UF
    cep_cliente: str = Column(String(10), nullable=True)  # CEP
    telefone_cliente: str = Column(String(20), nullable=True)  # Telefone do Cliente

    # Colunas que podem ser nulas (não obrigatórias)
    telefone_rec_cliente: str = Column(String(20), nullable=True)  # Telefone de recado
    whatsapp_cliente: str = Column(String(20), nullable=True)  # WhatsApp
    email_funcionario: str = Column(String(100), nullable=True)  # E-mail do Funcionário responsável
    acao: str = Column(String(255), nullable=True)  # Ação/observações adicionais
    fornecedor_cliente: str = Column(String(100), nullable=True)  # Fornecedor associado ao cliente

    # Colunas de datas
    data_cadastro_cliente: datetime = Column(DateTime, default=datetime.utcnow)  # Data de cadastro
    created_at: datetime = Column(DateTime, default=datetime.utcnow)  # Data de criação
    updated_at: datetime = Column(DateTime, onupdate=datetime.utcnow)  # Data de atualização
    usuario_id: int = Column(Integer, ForeignKey('usuario.id'))  # Chave estrangeira de usuários

    # Relacionamentos 1 para Muitos
    usuario: List[User]  = relationship("User", back_populates="clientes", uselist=True, lazy='joined')
    recebimentos: List[Recebimento]  = relationship("Recebimento", back_populates="cliente", lazy='joined')
    checklists: List[ChecklistRecebimento] = relationship("ChecklistRecebimento", back_populates="cliente", lazy='joined')

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
            # Carrega os relacionamentos e inclui se solicitado
            client_json["usuario"] = self.usuario_to_json() if self.usuario else None
            client_json["recebimentos"] = [self.recebimento_to_json(r) for r in self.recebimentos] if self.recebimentos else []
            client_json["checklists"] = [self.checklist_to_json(c) for c in self.checklists] if self.checklists else []

        return client_json

    def usuario_to_json(self):
        """Método para converter o relacionamento 'usuario' em JSON"""
        return {
            "id": self.usuario.id,
            "username": self.usuario.username,
            # Inclua outros campos que você deseja retornar do User
        }

    def recebimento_to_json(self, recebimento):
        """Método para converter o relacionamento 'recebimento' em JSON"""
        return {
            "id": recebimento.id,
            "valor": recebimento.valor,
            # Inclua outros campos que você deseja retornar de Recebimento
        }

    def checklist_to_json(self, checklist):
        """Método para converter o relacionamento 'checklist' em JSON"""
        return {
            "id": checklist.id,
            "status": checklist.status,
            # Inclua outros campos que você deseja retornar de ChecklistRecebimento
        }
