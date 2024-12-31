from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base  # Agora importa a base do SQLAlchemy de 'datapy'

class FotoRecebimento(Base):
    __tablename__ = 'foto_recebimento'  # Nome da tabela
    __table_args__ = {'extend_existing': True}  # Permite redefinir a tabela


    id = Column(Integer, primary_key=True)  # ID da Foto
    id_ordem = Column(String(50), nullable=False)  # ID da ordem (chave estrangeira)
    recebimento_id = Column(Integer, ForeignKey('recebimentos.id'), nullable=False)
    nome_foto = Column(String(255), nullable=False)  # Nome ou caminho do arquivo da foto
    
    # Relacionamento com a tabela Recebimento
    ordem = relationship("Recebimento", back_populates="fotos")

    # Adicionando as colunas de data e hora
    created_at = Column(DateTime, default=datetime.utcnow)  # Data de criação
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Data de última atualização
    deleted_at = Column(DateTime, nullable=True)  # Data de exclusão (opcional para soft delete)

    def __repr__(self):
        return f'<FotoRecebimento {self.id_ordem} - {self.nome_foto}>'
