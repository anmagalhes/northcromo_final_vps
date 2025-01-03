# app/schemas/componente.py
from pydantic import BaseModel
from typing import List, Optional

from app.models.postotrabalho import Postotrabalho

class PostotrabalhoSchema(BaseModel):
    name: str

class PostotrabalhoPublic(PostotrabalhoSchema):
    id: int

class PostotrabalhoList(BaseModel):
    postotrabalhos: list[PostotrabalhoPublic]
    offset: int
    limit: int

class PostotrabalhoUpdate(BaseModel):
    name: str | None = None