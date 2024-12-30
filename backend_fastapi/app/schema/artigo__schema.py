from typing import Optional

from pydantic import BaseModel


class ArtigoSchema(BaseModel):
    id: Optional[int] = None
    titulo: str
    usuario_id: Optional[int]

    class Config:
        from_attributes = True
