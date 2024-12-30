from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base  # Agora importa a base do SQLAlchemy de 'datapy'

class TarefaProduto(Base):
    __tablename__ = 'tarefa_Produto'  # Nome da tabela no banco de dados
    __table_args__ = {'extend_existing': True}  # Permite redefinir a tabela
    

    id = Column(Integer, primary_key=True)
    nome = Column(String(200), unique=True, nullable=False)
    usuario_id = Column(Integer, ForeignKey('usuario.id'))  # Chave estrangeira para 'usuarios'

    # Relacionamento: Agora utilizando o nome correto da classe 'User' (não 'Usuario')
    usuario = relationship("User", back_populates='tarefa_produto', foreign_keys=[usuario_id], lazy='joined')

    # Adicionando as colunas de data e hora
    created_at = Column(DateTime, default=datetime.utcnow)  # Data de criação
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Data de última atualização
    deleted_at = Column(DateTime, nullable=True)  # Data de exclusão (opcional para soft delete)

    def __repr__(self):
        return f'<TarefaProduto {self.nome}>'
