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


# Enum para o Status da Tarefa
class TaskStatus(str, Enum):
    pending = "Pending"
    in_progress = "In Progress"
    completed = "Completed"


# Modelo de Tarefa


class Task(BaseModel):
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.pending


# Modelo de Ordem de Serviço


class ServiceOrder(BaseModel):
    title: str
    description: Optional[str] = None
    tasks: List[Task] = []


# Banco de dados fictício (em memória para exemplo)
db_service_orders = []

# Rota para criar uma nova ordem de serviço


@app.post("/orders/", response_model=ServiceOrder)
async def create_order(order: ServiceOrder):
    order_id = str(uuid4())  # Gerar um ID único para a ordem
    db_service_orders.append({"id": order_id, **order.dict()})
    return {**order.dict(), "id": order_id}


# Rota para listar todas as ordens de serviço


@app.get("/orders/", response_model=List[ServiceOrder])
async def get_orders():
    return db_service_orders


# Rota para obter uma ordem de serviço específica


@app.get("/orders/{order_id}", response_model=ServiceOrder)
async def get_order(order_id: str):
    for order in db_service_orders:
        if order["id"] == order_id:
            return order
    raise HTTPException(status_code=404, detail="Order not found")


# Rota para adicionar uma tarefa a uma ordem de serviço


@app.post("/orders/{order_id}/tasks/", response_model=Task)
async def add_task_to_order(order_id: str, task: Task):
    for order in db_service_orders:
        if order["id"] == order_id:
            order["tasks"].append(task.dict())
            return task
    raise HTTPException(status_code=404, detail="Order not found")


# Rota para atualizar o status de uma tarefa


@app.put("/orders/{order_id}/tasks/{task_id}/", response_model=Task)
async def update_task_status(order_id: str, task_id: int, status: TaskStatus):
    for order in db_service_orders:
        if order["id"] == order_id:
            if 0 <= task_id < len(order["tasks"]):
                order["tasks"][task_id]["status"] = status
                return order["tasks"][task_id]
            raise HTTPException(status_code=404, detail="Task not found")
    raise HTTPException(status_code=404, detail="Order not found")
