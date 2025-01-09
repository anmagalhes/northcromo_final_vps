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
    Float,
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
class StatusOrdem(enum.Enum):
    PENDENTE = "PENDENTE"  # Status 1 - Pendente
    FINALIZADO = "FINALIZADO"  # Status 5 - Finalizado
    CANCELADO = "CANCELADO"  # Status 3 - Cancelado
    EM_ANDAMENTO = "EM_ANDAMENTO"


# Enum para Status da Tarefa
class StatusTarefaEnum(enum.Enum):
    PENDENTE = "PENDENTE"
    EM_ANDAMENTO = "EM_ANDAMENTO"
    FINALIZADO = "FINALIZADO"


class Recebimento(settings.Base):
    __tablename__ = "recebimentos"
    __table_args__ = {"extend_existing": True}

    # Campos básicos
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    tipo_ordem: Mapped[TipoOrdemEnum] = mapped_column(
        Enum(TipoOrdemEnum), nullable=True, default=TipoOrdemEnum.NAO
    )
    numero_ordem: Mapped[int] = mapped_column(
        Integer, nullable=True, index=True
    )  # NUMERO DA ORDEM NOVO
    recebimento_ordem: Mapped[str | None] = mapped_column(String(12), nullable=True)

    queixa_cliente: Mapped[str | None] = mapped_column(Text, nullable=True)
    data_prazo_desmont: Mapped[Optional[datetime]] = mapped_column(Date, nullable=True)

    referencia_produto: Mapped[str | None] = mapped_column(Text, nullable=True)

    numero_nota_fiscal: Mapped[str | None] = mapped_column(
        String(20), nullable=True
    )  # Campo adicional

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
        DateTime(timezone=True), nullable=True
    )
    hora_final_ordem: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Imagens relacionadas à ordem (Opcional)
    img1_ordem: Mapped[Optional[str]] = mapped_column(
        String(500), nullable=True
    )  # Caminho para a imagem 1
    img2_ordem: Mapped[Optional[str]] = mapped_column(
        String(500), nullable=True
    )  # Caminho para a imagem 2
    img3_ordem: Mapped[Optional[str]] = mapped_column(
        String(500), nullable=True
    )  # Caminho para a imagem 3
    img4_ordem: Mapped[Optional[str]] = mapped_column(
        String(500), nullable=True
    )  # Caminho para a imagem 4

    # Relacionamento com ItensRecebimento
    itens: Mapped[List["ItensRecebimento"]] = relationship(
        "ItensRecebimento",
        back_populates="recebimento",
        cascade="all, delete",
    )

    # Relacionamento Muitos-para-Muitos com NotaFiscal via tabela intermediária
    notas_fiscais: Mapped[List["NotaFiscal"]] = relationship(
        "NotaFiscal",
        secondary="nota_recebimento",  # Tabela intermediária
        back_populates="recebimentos",  # Relacionamento reverso
        cascade="all, delete",
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
        cascade="all, delete",
    )

    # Relacionamento Muitos-para-Um com Cliente
    cliente_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("clientes.id"), nullable=True
    )  # Adiciona o campo id_cliente

    # Relacionamento Many-to-One com Cliente
    cliente: Mapped["Cliente"] = relationship(
        "Cliente",  # A classe de destino
        back_populates="recebimentos",  # Nome da propriedade no modelo Cliente
        cascade="all, delete",
    )

    # Relacionamento com o Checklist
    checklists: Mapped[List["Checklist_Recebimento"]] = relationship(
        "Checklist_Recebimento",  # Relacionamento com Recebimento (um-para-muitos)
        back_populates="recebimento",  # Referência ao campo `usuario` em Recebimento
        uselist=False,  # Isso permite que seja uma lista de objetos Operacao
        cascade="all, delete",
    )

    status_ordem = StatusOrdem.PENDENTE

    def criar_item_inicial(self):
        """
        Cria o primeiro item de recebimento automaticamente após criar o recebimento.
        O item é deixado vazio para ser preenchido pelo usuário depois.
        """
        from app.models.recebimento.itens_recebimento import ItensRecebimento

        # Verificando se referencia_produto tem valor
        if not self.referencia_produto:
            raise ValueError("Referência do produto não pode ser vazia.")

        item = ItensRecebimento(
            recebimento_id=self.id,
            status_ordem=StatusOrdem.PENDENTE,  # Status inicial
            qtd_produto=0,  # Inicialmente a quantidade é 0
            preco_unitario=0.0,  # Inicialmente o preço unitário é 0
            preco_total=0.0,  # Preço total é 0
        )

        self.itens.append(item)  # Adicionando o item à lista de itens do recebimento

    def criar_checklist_inicial(self):
        """
        Cria o checklist inicial automaticamente após criar o recebimento.
        O checklist é relacionado a este recebimento com informações gerais.
        """
        from app.models.checklist_recebimento.checklist_recebimento import (
            Checklist_Recebimento,
        )

        # Verificando se referencia_produto tem valor
        if not self.referencia_produto:
            raise ValueError("Referência do produto não pode ser vazia.")

        # Inicializando o cod_produto como None
        cod_produto = None

        # Acessando os itens relacionados ao recebimento
        for item in self.itens:
            if item.cod_produto > 0:  # Primeiro item válido com cod_produto > 0
                cod_produto = item.cod_produto
                break  # Encontrou o primeiro produto válido, sai do loop

        # Caso não tenha encontrado nenhum produto válido, podemos definir um valor padrão (ex: 0 ou None)
        if cod_produto is None:
            cod_produto = (
                0  # Ou você pode usar None dependendo do comportamento desejado
            )

        # Criar o checklist único para o recebimento
        checklist_item = Checklist_Recebimento(
            recebimento_id=self.id,  # Usando o ID do recebimento
            datarec_ordem_servicos=self.data_rec_ordem,
            hora_inicial_ordem=self.hora_inicial_ordem,
            # referencia_produto=self.referencia_produto,
            nota_interna=f"Nota {self.numero_ordem}",  # Número de nota interna
            observacao_checklist="Observação inicial",  # Observação padrão
            status_tarefa=StatusTarefaEnum.PENDENTE,  # Status inicial do checklist
            data_checklist_ordem_servicos=self.data_rec_ordem,
            cliente_id=self.cliente_id,
            usuario_id=self.usuario_id,  # ID do usuário relacionado
            cod_produto=cod_produto,  # Atribuindo o cod_produto encontrado ou 0
        )

        # Adiciona o checklist ao recebimento
        self.checklists.append(checklist_item)

    def __repr__(self):
        return f"<Recebimento id={self.id} tipo_ordem={self.tipo_ordem or 'Unnamed'} recebimento_ordem={self.recebimento_ordem or 'Unnamed'}>"

    def mudar_status(self, novo_status: StatusOrdem):
        """
        Altera o status do recebimento e, se o novo status for FINALIZADO ou CANCELADO,
        atualiza a data final do recebimento.
        """
        if novo_status in [StatusOrdem.FINALIZADO, StatusOrdem.CANCELADO]:
            if (
                not self.data_final_ordem
            ):  # Garantir que data_final_ordem não foi preenchida ainda
                self.data_final_ordem = datetime.now(SP_TZ)

        self.status_ordem = novo_status  # Alterar o status

    def verificar_status_itens_e_atualizar(self):
        """
        Verifica todos os itens do recebimento. Se todos os itens não estiverem mais
        no status 'PENDENTE', altera o status do recebimento para 'FINALIZADO'.
        """
        todos_finalizados = all(
            item.status_ordem != StatusOrdem.PENDENTE for item in self.itens
        )

        if todos_finalizados:
            self.status_ordem = StatusOrdem.FINALIZADO
            self.data_final_ordem = datetime.now(SP_TZ)  # Definir data de finalização

    def __repr__(self):
        return f"<Recebimento id={self.id} tipo_ordem={self.tipo_ordem or 'Unnamed'} recebimento_ordem={self.recebimento_ordem or 'Unnamed'}>"
