from typing import Optional
from sqlmodel import Field, SQLModel

class Teste(SQLModel, table=True): 
     __tablename__= 'Producao'
     __table_args__ = {'extend_existing': True}  # Permite redefinir a tabela


     id: Optional[int] = Field(default=None, primary_key=True)
     titulo: str
     aulas: int
     horas: int
