# app/routes/cliente.py
from http import HTTPStatus
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.cliente.services import list_clientes, get_cliente, create_cliente, update_cliente, delete_cliente

# Instanciando o APIRouter
cliente_router = APIRouter()

# Dependência para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Rota para listar todos os clientes
@cliente_router.get("/", response_model=list[ClienteSchema])
async def get_all_clientes(db: Session = Depends(get_db)):
    """Retorna todos os clientes cadastrados."""
    return list_clientes(db)

# Rota para pegar detalhes de um cliente específico
@cliente_router.get("/{id}", response_model=ClienteSchema)
async def get_cliente_details(id: int, db: Session = Depends(get_db)):
    """Retorna os detalhes de um cliente pelo ID."""
    cliente = get_cliente(id, db)
    if cliente:
        return cliente
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Cliente não encontrado")

# Rota para criar um novo cliente
@cliente_router.post("/", response_model=ClienteSchema, status_code=HTTPStatus.CREATED)
async def criar_cliente(cliente_data: ClienteSchema, db: Session = Depends(get_db)):
    """Cria um novo cliente."""
    try:
        cliente = create_cliente(cliente_data.dict(), db)  # Passando os dados como dicionário
        return cliente
    except ValueError as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Erro ao criar cliente")

# Rota para atualizar um cliente
@cliente_router.put("/{id}", response_model=ClienteSchema)
async def update_cliente_details(id: int, cliente_data: ClienteSchema, db: Session = Depends(get_db)):
    """Atualiza os dados de um cliente específico."""
    cliente = get_cliente(id, db)
    if not cliente:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Cliente não encontrado")
    updated_cliente = update_cliente(id, cliente_data.dict(), db)
    if updated_cliente:
        return updated_cliente
    raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Erro ao atualizar cliente")

# Rota para deletar um cliente
@cliente_router.delete("/{id}")
async def delete_cliente_by_id(id: int, db: Session = Depends(get_db)):
    """Deleta um cliente pelo ID."""
    if delete_cliente(id, db):
        return {"message": "Cliente excluído com sucesso!"}
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Cliente não encontrado")
