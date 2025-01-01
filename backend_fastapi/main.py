# from app.core.database import init_db
import os
import sys
from enum import Enum
from typing import List, Optional
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "app")))

from app.routes import todo, user

# Definição do FastAPI
app = FastAPI()

# Registra os controladores de rotas
app.include_router(user.router)
app.include_router(todo.router)


# app.include_router(produto.router)
# app.include_router(order_controller.router)
# app.include_router(tarefa.router)
# app.include_router(checklist_recebimento.router)
# app.include_router(artigo.router)
