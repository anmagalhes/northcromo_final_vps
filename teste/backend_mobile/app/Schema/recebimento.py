from __future__ import annotations
from datetime import datetime, date
from typing import Optional, List, TYPE_CHECKING

from sqlalchemy import Integer, String, DateTime, Text, Date, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.config import settings
from app.utils.datetime import get_current_time_in_sp
from app.api.models.enums import SimNaoEnum, TipoOrdemEnum
from app.api.models.mixins import TimestampMixin


class Recebimento(settings.Base, TimestampMixin):
    __tablename__ = "recebimentos"
    __table_args__ = {"extend_existing": True}
    __allow_unmapped__ = True

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # Informações da ordem
    tipo_ordem: Mapped[Optional[TipoOrdemEnum]] = mapped_column(
        Enum(TipoOrdemEnum), default=TipoOrdemEnum.NAO
    )
    numero_ordem: Mapped[Optional[int]] = mapped_column(index=True)
    recebimento_ordem: Mapped[Optional[str]] = mapped_column(String(12))

    # Produto
    referencia_produto: Mapped[Optional[str]] = mapped_column(Text)
    numero_nota_fiscal: Mapped[Optional[str]] = mapped_column(String(20))

    # Queixa e prazo
    queixa_cliente: Mapped[Optional[str]] = mapped_column(Text)
    data_prazo_desmont: Mapped[Optional[date]] = mapped_column(Date)

    # Checklist
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

    # Datas e horários
    data_rec_ordem: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=get_current_time_in_sp
    )
    hora_inicial_ordem: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True)
    )
    data_final_ordem: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True)
    )
    hora_final_ordem: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True)
    )

    # Imagens
    img1_ordem: Mapped[Optional[str]] = mapped_column(String(500))
    img2_ordem: Mapped[Optional[str]] = mapped_column(String(500))
    img3_ordem: Mapped[Optional[str]] = mapped_column(String(500))
    img4_ordem: Mapped[Optional[str]] = mapped_column(String(500))
