#app/api/models/recebimento.py
from __future__ import annotations
from datetime import datetime, date
from typing import Optional

from sqlalchemy import ForeignKey, Integer, String, DateTime, Text, Date, Enum, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.utils.datetime import utcnow
from app.api.models.enums import SimNaoEnum, TipoOrdemEnum
from app.api.models.mixins import TimestampMixin
from app.api.models.base import Base

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.api.models.checklist_recebimento import ChecklistRecebimento
    from app.api.models.notafiscal import NotaFiscal

class Recebimento(Base, TimestampMixin):  # <-- usa Base do app.db.base
    __tablename__ = "recebimentos"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="Identificador único do recebimento"
    )

    #usuario_id: Mapped[int] = mapped_column(
    #    ForeignKey("usuarios.id"),
    #    index=True,
    #    comment="ID do usuário responsável pelo recebimento"
    #)
   # usuario: Mapped[Usuario] = relationship(back_populates="recebimentos")

    tipo_ordem: Mapped[TipoOrdemEnum] = mapped_column(
        Enum(TipoOrdemEnum),
        default=TipoOrdemEnum.NAO,
        nullable=False,
        comment="Tipo de ordem de serviço"
    )
    numero_ordem: Mapped[int] = mapped_column(
        Integer,
        index=True,
        nullable=True,
        comment="Número único da ordem de serviço"
    )
    recebimento_ordem: Mapped[str] = mapped_column(
        String(12),
        unique=True,
        nullable=True,
        comment="Código único de recebimento"
    )

    os_formatado: Mapped[str] = mapped_column(
        String(10),
        unique=False,
        index=True,
        nullable=True,
        comment="Número os Data"
    )

    referencia_produto: Mapped[str] = mapped_column(
        String(100),
        nullable=True,
        comment="Referência do produto conforme sistema ERP"
    )

    nota_fiscal_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("notas_fiscais.id"),
        nullable=True,
        index=True,  # Adicione index para melhor performance
        comment="Vinculo com nota fiscal"
    )

    nota_fiscal: Mapped[Optional["NotaFiscal"]] = relationship(
        "NotaFiscal",
        back_populates="recebimentos"
    )

    queixa_cliente: Mapped[str] = mapped_column(
        Text,
        nullable=True,
        comment="Descrição detalhada da queixa do cliente"
    )
    data_prazo_desmontagem: Mapped[date] = mapped_column(
        Date,
        nullable=True,
        comment="Data limite para conclusão da desmontagem"
    )

    sv_desmontagem_ordem: Mapped[SimNaoEnum] = mapped_column(
        Enum(SimNaoEnum),
        default=SimNaoEnum.NAO,
        nullable=True
    )
    sv_montagem_teste_ordem: Mapped[SimNaoEnum] = mapped_column(
        Enum(SimNaoEnum),
        default=SimNaoEnum.NAO,
        nullable=True
    )
    limpeza_quimica_ordem: Mapped[SimNaoEnum] = mapped_column(
        Enum(SimNaoEnum),
        default=SimNaoEnum.NAO,
        nullable=True
    )
    laudo_tecnico_ordem: Mapped[SimNaoEnum] = mapped_column(
        Enum(SimNaoEnum),
        default=SimNaoEnum.NAO,
        nullable=True
    )
    desmontagem_ordem: Mapped[SimNaoEnum] = mapped_column(
        Enum(SimNaoEnum),
        default=SimNaoEnum.NAO,
        nullable=True
    )

    data_recebimento: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utcnow,
        nullable=False,
        server_default=func.now(),
        comment="Data e hora do recebimento automático"
    )
    data_inicio_processo: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        comment="Data e hora de início do processamento"
    )
    data_conclusao_processo: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        comment="Data e hora de conclusão do processamento"
    )

    img1_ordem: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        comment="URL ou caminho da foto 1"
    )

    img2_ordem: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        comment="URL ou caminho da foto 2"
    )

    img3_ordem: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        comment="URL ou caminho da foto 3"
    )

    img4_ordem: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        comment="URL ou caminho da foto 4"
    )

    cliente: Mapped[str] = mapped_column(
            String(100),
            nullable=True,
            comment="Nome do cliente"
        )

    quantidade: Mapped[int] = mapped_column(
        Integer,
        nullable=True,  # ou False, dependendo se esse campo é obrigatório
        comment="Quantidade associada"
    )


     # Relacionamentos entre Recebimento
    # Relação com o checklist
    checklist: Mapped[Optional["ChecklistRecebimento"]] = relationship(
        "ChecklistRecebimento", back_populates="recebimento", uselist=False, cascade="all, delete"
    )


