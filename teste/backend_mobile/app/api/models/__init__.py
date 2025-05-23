# app/api/models/__init__.py

from app.api.models.base import Base  # Base declarativa

# Importar modelos
from app.api.models.cliente import Cliente
from app.api.models.usuario import Usuario
from app.api.models.recebimento import Recebimento
from app.api.models.checklist_recebimento import ChecklistRecebimento

__all__ = [
    "Base",
    "Cliente",
    "Usuario",
    "Recebimento",
    "ChecklistRecebimento",
]
