from pydantic import BaseModel
from typing import Optional


class VendedorResponse(BaseModel):
    id_vendedor: int
    nome_vendedor: str
    email_vendedor: Optional[str]

    class Config:
        orm_mode = True
