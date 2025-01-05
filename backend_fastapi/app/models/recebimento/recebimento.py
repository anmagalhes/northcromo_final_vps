# app/models/recebimento/recebimento.py
from datetime import datetime
import pytz
from sqlalchemy import (
    Enum,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Boolean,
    Text,
    Date,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.config import settings
from typing import Optional, List
import enum

# Criando um timezone para São Paulo (UTC-3)
SP_TZ = pytz.timezone("America/Sao_Paulo")


# Função auxiliar para garantir o uso correto do timezone
def get_current_time_in_sp() -> datetime:
    return datetime.now(SP_TZ).astimezone(
        SP_TZ
    )  # Garante que a data e hora sejam "aware"


# Definindo ENUMs para os campos SIM/NAO
class SimNaoEnum(enum.Enum):
    SIM = "SIM"
    NAO = "NAO"


class Recebimento(settings.Base):
    __tablename__ = "recebimentos"
    __table_args__ = {"extend_existing": True}

    # Campos básicos
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tipo_ordem: Mapped[str] = mapped_column(String(20), nullable=False)
    recebimento_ordem: Mapped[int] = mapped_column(String(12), nullable=False)
    Referencia_Produto: Mapped[str | None] = mapped_column(Text, nullable=False)
    queixa_cliente: Mapped[str | None] = mapped_column(Text, nullable=False)
    data_prazo_desmont: Mapped[Optional[datetime]] = mapped_column(Date, nullable=False)

    # Para o checklist
    sv_desmontagem_ordem: Mapped[SimNaoEnum] = mapped_column(
        Enum(SimNaoEnum), default=SimNaoEnum.NAO
    )
    sv_montagem_teste_ordem: Mapped[SimNaoEnum] = mapped_column(
        Enum(SimNaoEnum), default=SimNaoEnum.NAO
    )
    limpeza_quimica_ordem: Mapped[SimNaoEnum] = mapped_column(
        Enum(SimNaoEnum), default=SimNaoEnum.NAO
    )
    laudo_tecnico_ordem: Mapped[SimNaoEnum] = mapped_column(
        Enum(SimNaoEnum), default=SimNaoEnum.NAO
    )
    desmontagem_ordem: Mapped[SimNaoEnum] = mapped_column(
        Enum(SimNaoEnum), default=SimNaoEnum.NAO
    )

    # Campos de data e hora
    data_rec_ordem: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=get_current_time_in_sp
    )
    hora_inicial_ordem: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    data_final_ordem: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    hora_final_ordem: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )

    # Imagens relacionadas à ordem (Opcional)
    img1_ordem: Mapped[Optional[str]] = mapped_column(
        String(500), nullable=False
    )  # Caminho para a imagem 1
    img2_ordem: Mapped[Optional[str]] = mapped_column(
        String(500), nullable=False
    )  # Caminho para a imagem 2
    img3_ordem: Mapped[Optional[str]] = mapped_column(
        String(500), nullable=False
    )  # Caminho para a imagem 3
    img4_ordem: Mapped[Optional[str]] = mapped_column(
        String(500), nullable=False
    )  # Caminho para a imagem 4

    # Relacionamento com Produto (muitos para muitos)
    produtos: Mapped[List["Produto"]] = relationship(
        "Produto",  # Nome da classe relacionada
        secondary="itens_recebimento",  # Tabela intermediária para o relacionamento muitos-para-muitos
        back_populates="recebimentos",
    )

    # Relacionamento com ItensRecebimento
    itens: Mapped[List["ItensRecebimento"]] = relationship(
        "ItensRecebimento",
        back_populates="recebimento",
    )

    # Relacionamento Muitos-para-Muitos com NotaFiscal via tabela intermediária
    notas_fiscais: Mapped[List["NotaFiscal"]] = relationship(
        "NotaFiscal",
        secondary="nota_recebimento",  # Tabela intermediária
        back_populates="recebimentos",  # Relacionamento reverso
    )

    # Colunas de controle de data
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=get_current_time_in_sp
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=get_current_time_in_sp,
        onupdate=get_current_time_in_sp,
    )
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # Relacionamento com o modelo User (usando tipagem de string)
    usuario_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("usuario.id"), nullable=True
    )  # Tabela Campo

    # Relacionamento MANY-TO-ONE de Grupo_Produto para User (não 'Usuario')
    usuario: Mapped["User"] = relationship(
        "User",  # Referência correta à classe 'User'
        back_populates="recebimentos",  # Nome do campo de volta no User
        lazy="joined",
    )

    # Relacionamento Muitos-para-Um com Cliente
    cliente_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("clientes.id"), nullable=False
    )  # Adiciona o campo id_cliente

    # Relacionamento Many-to-One com Cliente
    cliente: Mapped["Cliente"] = relationship(
        "Cliente",  # A classe de destino
        back_populates="recebimentos",  # Nome da propriedade no modelo Cliente
        lazy="joined",
    )

    # Relacionamento com o Checklist
    checklists: Mapped[List["Checklist_Recebimento"]] = relationship(
        "Checklist_Recebimento",  # Relacionamento com Recebimento (um-para-muitos)
        back_populates="recebimento",  # Referência ao campo `usuario` em Recebimento
        lazy="joined",
        uselist=True,  # Isso permite que seja uma lista de objetos Operacao
    )

    def __repr__(self):
        return f"<Recebimento id={self.id} tipo_ordem={self.tipo_ordem or 'Unnamed'} recebimento_ordem={self.recebimento_ordem or 'Unnamed'}>"
