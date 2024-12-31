from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm import relationship
from app.database import Base  # Agora importa a base do SQLAlchemy de 'datapy'

class Funcionario(Base):
    __tablename__ = 'funcionarios'  # Nome da tabela no banco de dados
    __table_args__ = {'extend_existing': True}  # Permite redefinir a tabela


    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    telefone = Column(String(15), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    funcao = Column(String(50), nullable=False)
    setor = Column(String(50), nullable=False)
    data_cadastro = Column(DateTime, default=datetime.utcnow)
    acesso_sistema = Column(Boolean, default=True)  # Se tem acesso ao sistema
    usuario_id = Column(Integer, ForeignKey('usuario.id'))  # Chave estrangeira de usuários
 
    nivel_acesso = Column(String(50), nullable=False)  # Nível de acesso do funcionário
    acao = Column(String(100), nullable=True)  # Ações/observações adicionais
    
    # Relacionamento: Agora utilizando o nome correto da classe 'User' (não 'Usuario')
    usuario = relationship("User", back_populates='funcionarios', foreign_keys=[usuario_id], lazy='joined')


    # Relacionamento com Recebimentos (como vendedor, por exemplo)
    recebimentos_cadastrados = relationship(
        "Recebimento", 
        back_populates="funcionario",  # O 'back_populates' na classe Recebimento já foi configurado corretamente
        uselist=True,  # Relação de um-para-muitos
        lazy='joined'  # Lazy loading para otimizar a carga dos dados
    )

    def __repr__(self):
        return f'<Funcionario id={self.id} name={self.name}>'
