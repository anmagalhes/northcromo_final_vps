#app/models/produto.py
from datetime import datetime
import pytz
from sqlalchemy import (
    Integer,
    String,
    ForeignKey,
    DateTime,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.config import settings
from typing import Optional, List

# Criando um timezone para São Paulo (UTC-3)
SP_TZ = pytz.timezone("America/Sao_Paulo")


# Função auxiliar para garantir o uso correto do timezone
def get_current_time_in_sp() -> datetime:
    return datetime.now(SP_TZ).astimezone(
        SP_TZ
    )  # Garante que a data e hora sejam "aware"


class Produto(settings.Base):
    __tablename__ = "produtos"
    __table_args__ = {"extend_existing": True}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    codigo: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    nome_produto: Mapped[str] = mapped_column(String(300), unique=True, nullable=False)
    und_servicos: Mapped[str] = mapped_column(String(5), unique=True, nullable=False)

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
        back_populates="produtos",  # Nome do campo de volta no User
        lazy="joined",
    )

    # Relacionamento com o modelo Componente
    componente_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("componentes.id"), nullable=True
    )  # Tabela Campo

    # Relacionamento MANY-TO-ONE de Grupo_Produto para User (não 'Usuario')
    componentes: Mapped["Componente"] = relationship(
        "Componente",  # Referência correta à classe 'User'
        back_populates="produtos",  # Nome do campo de volta no User
        lazy="joined",
    )

    # Relacionamento com o modelo Componente
    operacao_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("operacacoes.id"), nullable=True
    )  # Tabela Campo

     # Relacionamento com 'Operacao' (caso esteja faltando)
    Operacoes: Mapped["Operacao"] = relationship(
        "Operacao",  # Nome da classe de destino
        back_populates="produtos",  # Nome do campo de volta em Operacao
        lazy="joined",  # Carregamento desejado
        uselist=True  # Isso permite que seja uma lista de objetos Operacao
    )

     # Relacionamento com o modelo Componente
    grupo_produto_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("grupo_produto.id"), nullable=True
    )  # Tabela Campo

     # Relacionamento com 'Operacao' (caso esteja faltando)
    grupo_produtos: Mapped["Grupo_Produto"] = relationship(
        "Grupo_Produto",  # Nome da classe de destino
        back_populates="produtos",  # Nome do campo de volta em Operacao
        lazy="joined",  # Carregamento desejado
        uselist=True  # Isso permite que seja uma lista de objetos Operacao
    )

    # Relacionamento com o modelo posto_trabalho
    posto_trabalho_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("Postotrabalho_novos.id"), nullable=True
    )  

    # Relacionamento MANY-TO-ONE de Grupo_Produto para User (não 'Usuario')
    Postotrabalhos: Mapped["Postotrabalho"] = relationship(
        "Postotrabalho",  # Certifique-se de usar o nome correto da classe (Postotrabalho)
        back_populates="produtos",  # Nome do campo de volta em Postotrabalho
        lazy="joined",
    )
    
    def __repr__(self):
        return f'<Produto id={self.id} nome_produto={self.nome_produto if self.nome_produto else "Unnamed"}>'
