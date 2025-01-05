from pydantic import BaseModel
from typing import Optional

class ClienteResponse(BaseModel):
    id_cliente: int
    nome_cliente: str
    cpf_cliente: Optional[str]
    email_cliente: Optional[str]

    class Config:
        orm_mode = True
