
from pydantic import BaseModel
from typing import List, Optional
from schema.task_schema import TaskSchema

class ArtigoSchema(BaseModel):
    id: Optional[int] = None
    titulo: str
    usuario_id : Optional[int]

    class Config:
        orm_mode = True