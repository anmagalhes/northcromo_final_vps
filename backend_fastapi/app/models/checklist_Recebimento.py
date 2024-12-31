# app/models/Checklist_Recebimento.py
from datetime import datetime
import pytz

from sqlalchemy import JSON, Boolean, DateTime, ForeignKey, Integer, String, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import List, Optional

from app.core.config import settings

# Criando um timezone para São Paulo (UTC-3)
SP_TZ = pytz.timezone("America/Sao_Paulo")

class ChecklistRecebimento(settings.Base):  # Substituindo Base de 'datapy' para o Base do app
    __tablename__ = 'checklist_recebimento'
    __table_args__ = {'extend_existing': True}  # Permite redefinir a tabela

    # Usando Mapped e mapped_column para definir as colunas
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_Recebimento: Mapped[int] = mapped_column(Integer, ForeignKey('recebimentos.id'), nullable=False)  # ID do recebimento
    id_cliente: Mapped[int] = mapped_column(Integer, ForeignKey('cliente.id'), nullable=False)  # ID do cliente
    qtd_Produto: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)  # Quantidade do produto
    cod_Produto: Mapped[int] = mapped_column(Integer, ForeignKey('produtos.id'), nullable=False)  # Código do produto
    referencia_Produto: Mapped[str] = mapped_column(String(50), nullable=False)  # Referência do produto
    notaInterna: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)  # Nota interna (opcional)
    qUEIXA_CLIENTE: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)  # Queixa do cliente (opcional)
    dataChecklist_OrdemServicos: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=lambda: datetime.now(SP_TZ))  # Data do checklist
    usuario_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('usuario.id'))  # Chave estrangeira de usuários
    LINK_PDF_CHECKLIST: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)  # Link do PDF do checklist
    Status_Checklist: Mapped[str] = mapped_column(String(50), nullable=False)  # Status do checklist (ex: 'Concluído', 'Em andamento', etc.)

    # Relacionamentos
    recebimento: Mapped["Recebimento"] = relationship("Recebimento", back_populates="checklists")
    cliente: Mapped["Cliente"] = relationship("Cliente", back_populates="checklists")
    produto: Mapped["Produto"] = relationship("Produto", back_populates="checklists")
    usuario: Mapped["User"] = relationship("User", back_populates="checklists")
    
    # Relacionamento com ImpressaoChecklistRecebimento
    impressao_checklists: Mapped[list] = relationship("ImpressaoChecklistRecebimento", lazy=True)

    # Colunas de data e hora
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(SP_TZ))  # Data de criação
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(SP_TZ), onupdate=lambda: datetime.now(SP_TZ))  # Data de última atualização
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)  # Data de exclusão (opcional para soft delete)

    def __repr__(self):
        # Acessando o nome do produto carregado (mesmo com o lazy load)
        produto_nome = self.produto.nome if self.produto else 'Produto não encontrado'
        return f'<ChecklistRecebimento {self.referencia_Produto} - {produto_nome}>'
