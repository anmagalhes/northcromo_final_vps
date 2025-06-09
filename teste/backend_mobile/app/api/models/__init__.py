# app/api/models/__init__.py
#python create_tables.py

from app.api.models.base import Base  # Base declarativa

# Importar modelos
from app.api.models.cliente import Cliente
from app.api.models.usuario import Usuario
from app.api.models.recebimento import Recebimento
from app.api.models.checklist_recebimento import ChecklistRecebimento
from app.api.models.componente import Componente
from app.api.models.operacao import Operacao
from app.api.models.posto_trabalho import Posto_Trabalho
from app.api.models.defeito import Defeito


# python create_tables.py
__all__ = [
    "Base",
    "Cliente",
    "Usuario",
    "Recebimento",
    "ChecklistRecebimento",
    "Componente",
    "Operacao",
    "Posto_Trabalho",
    "Defeito"
]
