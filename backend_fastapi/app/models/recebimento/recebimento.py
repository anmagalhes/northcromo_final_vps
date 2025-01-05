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

# Definindo o Enum para tipo_ordem
class TipoOrdemEnum(enum.Enum):
    NOVO = "NOVO"
    NAO = "NAO"


# Definindo o Enum de StatusOrdem
class StatusOrdem(PyEnum):
    PENDENTE = 1  # Status 1 - Pendente
    FINALIZADO = 5  # Status 5 - Finalizado
    CANCELADO = 3  # Status 3 - Cancelado
    EM_ANDAMENTO = 2  # Status 2 - Em Andamento

# Enum para Status da Tarefa
class StatusTarefaEnum(enum.Enum):
    PENDENTE = "PENDENTE"
    EM_ANDAMENTO = "EM_ANDAMENTO"
    FINALIZADO = "FINALIZADO"


class Recebimento(settings.Base):
    __tablename__ = "recebimentos"
    __table_args__ = {"extend_existing": True}

    # Campos básicos
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tipo_ordem: Mapped[TipoOrdemEnum] = mapped_column(
        Enum(TipoOrdemEnum), nullable=False, default=TipoOrdemEnum.NAO
    )
    numero_ordem: Mapped[int] = mapped_column(Integer, nullable=False)                   # NUMERO DA ORDEM NOVO
    recebimento_ordem: Mapped[str | None] = mapped_column(String(12), nullable=False)
    
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
        uselist=False,  # Isso permite que seja uma lista de objetos Operacao
    )

    def criar_item_inicial(self):
        """
        Cria o primeiro item de recebimento automaticamente após criar o recebimento.
        O item é deixado vazio para ser preenchido pelo usuário depois.
        """
        from app.models.recebimento.itens_recebimento import ItensRecebimento
        item = ItensRecebimento(
            recebimento_id=self.id,
            status_ordem=StatusOrdem.PENDENTE,  # Status inicial
            qtd_Produto=0,  # Inicialmente a quantidade é 0
            preco_unitario=0.0,  # Inicialmente o preço unitário é 0
            preco_total=0.0,  # Preço total é 0
            referencia_produto=None  # Inicialmente sem referência
            )
        self.itens.append(item)  # Adicionando o item à lista de itens do recebimento

    def criar_checklist_inicial(self):
        """
        Cria o checklist inicial automaticamente após criar o recebimento.
        O checklist é relacionado a este recebimento com informações gerais.
        """
        from app.models.checklist_recebimento.checklist_recebimento import Checklist_Recebimento

        # Criar o checklist único para o recebimento
        checklist_item = Checklist_Recebimento(
            recebimento_id=self.id,
            datarec_ordem_servicos=self.data_rec_ordem,
            hora_inicial_ordem=self.hora_inicial_ordem,
            referencia_produto="Referência geral",  # Pode ser um dado genérico
            nota_interna=f"Nota {self.numero_nota_fiscal}",
            observacao_checklist="Observação inicial",  # Pode ser preenchido depois
            status_tarefa=StatusTarefaEnum.PENDENTE,
            data_checklist_ordem_servicos=self.data_rec_ordem,
            cliente_id=self.cliente_id,
            usuario_id=self.usuario_id
        )
        self.checklists.append(checklist_item)  # Adiciona o checklist ao recebimento

    def __repr__(self):
        return f"<Recebimento id={self.id} tipo_ordem={self.tipo_ordem or 'Unnamed'} recebimento_ordem={self.recebimento_ordem or 'Unnamed'}>"