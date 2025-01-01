# app/models/cliente.py
from datetime import datetime
import pytz

from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.config import settings

# Criando um timezone para São Paulo (UTC-3)
SP_TZ = pytz.timezone("America/Sao_Paulo")


class Cliente(settings.Base):  # Substituímos db.Model por Base
    __tablename__ = "clientes"
    __table_args__ = {"extend_existing": True}  # Permite redefinir a tabela

    # Usando Mapped e mapped_column para definir as colunas
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    tipo_cliente: Mapped[str | None] = mapped_column(
        String(50), nullable=True
    )  # Tipo de Cliente
    nome_cliente: Mapped[str | None] = mapped_column(
        String(100), nullable=True
    )  # Nome do Cliente
    doc_cliente: Mapped[str | None] = mapped_column(
        String(20), nullable=True
    )  # Documento do Cliente (CPF/CNPJ)
    endereco_cliente: Mapped[str | None] = mapped_column(
        String(255), nullable=True
    )  # Endereço do Cliente
    num_cliente: Mapped[str | None] = mapped_column(
        String(20), nullable=True
    )  # Número do endereço
    bairro_cliente: Mapped[str | None] = mapped_column(
        String(100), nullable=True
    )  # Bairro
    cidade_cliente: Mapped[str | None] = mapped_column(
        String(100), nullable=True
    )  # Cidade
    uf_cliente: Mapped[str | None] = mapped_column(String(2), nullable=True)  # UF
    cep_cliente: Mapped[str | None] = mapped_column(String(10), nullable=True)  # CEP
    telefone_cliente: Mapped[str | None] = mapped_column(
        String(20), nullable=True
    )  # Telefone do Cliente

    # Colunas que podem ser nulas (não obrigatórias)
    telefone_rec_cliente: Mapped[str | None] = mapped_column(
        String(20), nullable=True
    )  # Telefone de recado
    whatsapp_cliente: Mapped[str | None] = mapped_column(
        String(20), nullable=True
    )  # WhatsApp
    email_funcionario: Mapped[str | None] = mapped_column(
        String(100), nullable=True
    )  # E-mail do Funcionário responsável
    acao: Mapped[str | None] = mapped_column(
        String(255), nullable=True
    )  # Ação/observações adicionais
    fornecedor_cliente: Mapped[str | None] = mapped_column(
        String(100), nullable=True
    )  # Fornecedor associado ao cliente

    # Relacionamento com o modelo User (usando tipagem de string)
    usuario_id: Mapped[int] = mapped_column(Integer, ForeignKey('usuario.id')) # Tabela Campo
       
    # Relacionamento MANY-TO-ONE de Grupo_Produto para User (não 'Usuario')
    usuario: Mapped["User"] = relationship(
            "User",  # Referência correta à classe 'User'
            back_populates="clientes",  # Nome do campo de volta no User
            lazy='joined'
        )

    # Colunas de datas
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(SP_TZ)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(SP_TZ),
        onupdate=lambda: datetime.now(SP_TZ),
    )
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True
    )  # Permite que seja None

    # Relacionamento com Recebimento - Importação tardia
    #recebimentos: Mapped[list["Recebimento"]] = relationship(
    #    "Recebimento", back_populates="clientes", lazy="joined"
   # )

    def __repr__(self):
        return f"<clientes {self.nome_cliente}>"
