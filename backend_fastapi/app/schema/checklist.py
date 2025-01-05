from pydantic import BaseModel

class ChecklistResponse(BaseModel):
    id_checklist: int
    descricao_checklist: str
    status_checklist: str  # Exemplo: "Pendente" ou "Concluído"

    class Config:
        orm_mode = True
